# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import asyncio
import json
import logging
import re
import shutil
import subprocess
from io import BytesIO
from pathlib import Path
from typing import Final, List, Optional, Set, Tuple

from aria_studio.app.common.disk_cache import DiskCache
from aria_studio.app.common.types import (
    AriaError,
    AriaException,
    CopyStatus,
    DeviceStatus,
    to_error_message,
)
from aria_studio.app.constants import DEVICE_CACHE_DIR, THUMBNAIL_GIF, THUMBNAIL_JPEG
from aria_studio.app.local.local_file_manager import LocalFileManager
from PIL import Image
from projectaria_tools.aria_mps_cli.cli_lib.common import log_exceptions

logger = logging.getLogger(__name__)

_ARIA_RECORDINGS_ROOT: Final[Path] = Path("/sdcard/recording")
_ARIA_THUMBNAILS_ROOT: Final[Path] = _ARIA_RECORDINGS_ROOT / "thumbnails"
_VRS_EXT: str = ".vrs"
_DEVICE_MONITOR_INTERVAL: int = 5
_ARIA_DEVICE_IDENTIFIER: str = "product:gemini model:Aria device:gemini"


class DeviceManager:
    """
    The class to manage the interaction with the Aria Device
    * Pull files from the device.
    * Delete files from the device.
    * List files on the device.
    * Fetch device status
        * Fetch Wi-Fi SSID
        * Fetch Bluetooth device name
        * Fetch battery status
    * Fetch thumbnails
    """

    adb_path_: Optional[str] = None

    instance_: Optional["DeviceManager"] = None

    @classmethod
    def get_instance(cls):
        """Get the individual mps request manager singleton."""
        if cls.instance_ is None:
            logger.debug("Creating device manager")
            cls.instance_ = DeviceManager()
        return cls.instance_

    @classmethod
    async def reset(cls):
        """Reset the device manager singleton."""
        async with cls.lock_:
            logger.debug("Resetting device manager")
            cls.instance_ = None

    @classmethod
    def set_adb_path(cls, adb_path: str):
        """Set the path to adb executable."""
        if not adb_path.is_file():
            raise FileNotFoundError(f"adb path {adb_path} does not exist")
        cls.adb_path_ = adb_path

    def __init__(self, max_concurrent_pulls: int = 1):
        self._copy_tasks: Set[asyncio.Task] = set()
        self._vrs_files_to_copy: List[Path] = []
        self._destination: Path = Path()
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(max_concurrent_pulls)
        self._copy_lock: asyncio.Lock = asyncio.Lock()
        self._copy_status: CopyStatus = CopyStatus()
        self._disk_cache: DiskCache = DiskCache(DEVICE_CACHE_DIR)
        self._device_monitor: asyncio.Task = asyncio.create_task(
            self.device_heartbeat()
        )

    @property
    def cache(self):
        return self._disk_cache

    async def check_device_connected(self):
        """Check if the device is connected."""
        stdout, stderr = await self._adb_command(["devices", "-l"])
        if _ARIA_DEVICE_IDENTIFIER not in stdout.decode("UTF-8"):
            raise AriaException(AriaError.DEVICE_NOT_CONNECTED, "Device not connected")

    @log_exceptions
    async def device_heartbeat(self):
        """
        Monitor the device status periodically and clear the cache if the device has
        been disconnected.
        """
        while True:
            try:
                await asyncio.sleep(_DEVICE_MONITOR_INTERVAL)
                # Ensure device connection
                await self.check_device_connected()
                logger.debug("Heartbeat connected")
            except Exception:
                logger.debug("Heartbeat not connected")
                # Clear the cache
                self._disk_cache.clear()

    async def get_status(self) -> DeviceStatus:
        """Get the status of the device"""
        # Ensure device connection
        await self.check_device_connected()

        # Query device status concurrently
        status_tasks = [
            self._adb_command(
                ["shell", "getprop", "ro.serialno"], AriaError.GET_STATUS_FAILED
            ),
            self._adb_command(
                ["shell", "dumpsys", "battery"], AriaError.GET_STATUS_FAILED
            ),
            self._adb_command(
                ["shell", "dumpsys", "wifi"], AriaError.GET_STATUS_FAILED
            ),
        ]
        status_results = await asyncio.gather(*status_tasks, return_exceptions=True)
        for result in status_results:
            if isinstance(result, AriaException):
                raise result
        serial_stdout, _ = status_results[0]
        battery_stdout, _ = status_results[1]
        wifi_stdout, _ = status_results[2]

        # Get Serial number
        serial_number: str = serial_stdout.decode("UTF-8").strip()

        # Get battery level
        match = re.search(r"level: (\d+)", battery_stdout.decode("UTF-8"))
        battery_level: int = int(match.group(1) if match else 0)

        # Get Wi-Fi SSID
        match = re.search(r"^ssid=(.*)$", wifi_stdout.decode("UTF-8"), re.MULTILINE)

        wifi_ssid: Optional[str] = match.group(1) if match else None

        return DeviceStatus(
            serial_number=serial_number,
            wifi_ssid=wifi_ssid,
            battery_level=battery_level,
            import_in_progress=bool(
                self._copy_tasks and any(not task.done() for task in self._copy_tasks)
            ),
        )

    @log_exceptions
    async def delete_files(self, vrs_files: List[str]) -> None:
        """Delete files from the device."""
        # Delete vrs files
        vrs_and_metadata_files: List[Path] = [
            Path(_ARIA_RECORDINGS_ROOT, f"{f}*") for f in vrs_files
        ]
        thumbnails: List[Path] = [
            _ARIA_THUMBNAILS_ROOT / f"{Path(f).stem}*" for f in vrs_files
        ]
        try:
            await self._adb_command(
                ["shell", "rm"] + vrs_and_metadata_files + thumbnails,
                AriaError.DELETE_FAILED,
            )
        except AriaException as e:
            if e.error_code == AriaError.DELETE_FAILED:
                logger.debug("No files found on device")
            else:
                raise

    @log_exceptions
    async def list_vrs_files(self) -> List[Path]:
        """List recordings on the device."""
        try:
            stdout, stderr = await self._adb_command(
                ["shell", "ls", Path(_ARIA_RECORDINGS_ROOT) / f"*{_VRS_EXT}"],
                AriaError.LIST_RECORDING_FAILED,
            )
        except AriaException as e:
            if e.error_code == AriaError.LIST_RECORDING_FAILED:
                logger.debug("No vrs files found on device")
                return []
            else:
                raise
        return [Path(p) for p in stdout.decode().splitlines()]

    async def _pull_file(
        self, file_path: Path, destination: Path, compress: bool = False
    ) -> Tuple[str, str]:
        """Pull a single file from the device."""
        return await self._adb_command(
            ["pull", file_path, destination], AriaError.PULL_FAILED
        )

    @log_exceptions
    async def get_thumbnail_jpeg(self, vrs_file: str) -> Path:
        """Get first thumbnail for the VRS file from ."""
        thumbnail_path = self._disk_cache.get_cache_dir(vrs_file) / THUMBNAIL_JPEG
        if thumbnail_path.exists():
            return thumbnail_path

        thumbnails: List[Path] = await self._list_thumbnails(vrs_file)
        # Copy any one thumbnail
        for thumbnail in thumbnails:
            try:
                img_data: str = await self._shell_cat(thumbnail)
                Image.open(BytesIO(img_data)).rotate(-90).save(thumbnail_path)
                return thumbnail_path
            except Exception as e:
                logger.exception(e)
                continue
        # Couldn't copy a thumbnail
        raise AriaException(
            AriaError.THUMBNAIL_NOT_FOUND, f"No thumbnail found for {vrs_file}"
        )

    @log_exceptions
    async def get_thumbnail_gif(self, vrs_file: str) -> Path:
        """Pull thumbnails and create a gif file from the thumbnails."""
        thumbnail_path = self._disk_cache.get_cache_dir(vrs_file) / THUMBNAIL_GIF
        if thumbnail_path.exists():
            return thumbnail_path

        thumbnails: List[Path] = await self._list_thumbnails(vrs_file)
        if not thumbnails:
            raise FileNotFoundError(f"No thumbnails found for {vrs_file}")
        # Read each thumbnail, rotate it and then add to gif
        rotated_images: List[Image] = []
        for thumbnail in thumbnails:
            try:
                img_data: str = await self._shell_cat(thumbnail)
                rotated_images.append(
                    Image.open(BytesIO(img_data)).rotate(-90).convert("RGBA")
                )
            except Exception as e:
                logger.exception(e)
                continue
        if not rotated_images:
            raise AriaException(
                AriaError.GIF_GENERATE_FAILED,
                f"Failed to generate gif for {vrs_file}",
            )
        rotated_images[0].save(
            thumbnail_path,
            save_all=True,
            append_images=rotated_images[1:],
            duration=500,  # Duration between frames in milliseconds
            loop=0,  # Loop forever
        )
        return thumbnail_path

    @log_exceptions
    async def get_metadata(self, vrs_file: str) -> Path:
        """Pull metadata file from device."""
        try:
            metadata = await self._shell_cat(
                (_ARIA_RECORDINGS_ROOT / f"{vrs_file}.json"),
                AriaError.METADATA_READ_FAILED,
            )
            return json.loads(metadata.decode("UTF-8"))
        except json.JSONDecodeError:
            raise AriaException(
                AriaError.METADATA_READ_FAILED, "Not a valid json metadata"
            )
        return None

    async def _shell_cat(
        self, file_path: Path, error_code: Optional[AriaError] = None
    ) -> str:
        """Helper to run adb shell cat command"""
        command = ["shell", "cat", file_path]
        stdout, stderr = await self._adb_command(command, error_code=error_code)
        return stdout

    async def _list_thumbnails(self, vrs_file: str) -> List[Path]:
        """List thumbnails for a VRS file."""
        thumbnail_pattern: str = f"{vrs_file[:-4]}_*.jpeg"
        # Return the modified path with the new stem and the .jpg extension
        thumbnail_path_on_aria: Path = _ARIA_THUMBNAILS_ROOT / thumbnail_pattern
        stdout, stderr = await self._adb_command(
            ["shell", "ls", thumbnail_path_on_aria],
            AriaError.LIST_THUMBNAIL_FAILED,
        )
        if not stdout:
            raise AriaException(AriaError.THUMBNAIL_NOT_FOUND)
        return [Path(p) for p in stdout.decode().splitlines()]

    #
    # Apis to copy files from device to local
    #
    @log_exceptions
    async def start_copy_vrs_files(
        self,
        vrs_files: List[str],
        destination: Path,
        delete_src_after_copy: bool = False,
    ):
        """Start copying files asynchronously."""
        async with self._copy_lock:
            if self._copy_tasks and any(not task.done() for task in self._copy_tasks):
                error_code = AriaError.VRS_PULL_IN_PROGRESS
                raise AriaException(error_code, to_error_message(error_code))

            self._copy_status = CopyStatus()
            for vrs_file in vrs_files:
                if not vrs_file.endswith(_VRS_EXT):
                    raise AriaException(
                        AriaError.NOT_A_VRS_FILE, f"{vrs_file} is not a VRS file"
                    )
                logger.debug(f"Checking if {vrs_file} exists locally at {destination}")
                if (destination / vrs_file).exists():
                    raise FileExistsError(
                        f"{vrs_file} already exists locally at {destination}"
                    )

            # It is now safe to start copying the files
            self._vrs_files_to_copy = [
                _ARIA_RECORDINGS_ROOT / vrs_file for vrs_file in vrs_files
            ]
            total_bytes = await self._get_total_size(self._vrs_files_to_copy)
            self._copy_status.total_bytes = total_bytes
            self._copy_status.total_files = len(self._vrs_files_to_copy)
            logger.debug(f"Total size of files to copy: {total_bytes}")
            self._destination = destination
            self._copy_monitor_task: asyncio.Task = asyncio.create_task(
                self._copy_monitor(
                    self._vrs_files_to_copy,
                    destination,
                    delete_src_after_copy,
                )
            )

    async def _copy_monitor(
        self,
        vrs_files_to_copy: List[str],
        destination: Path,
        delete_src_after_copy: bool,
    ):
        """Start and monitor the copy operation.
        This is a coroutine that runs in the background and updates progress."""
        for vrs_file in self._vrs_files_to_copy:
            t = asyncio.create_task(
                self._copy_vrs_and_metadata(
                    Path(vrs_file),
                    destination / vrs_file.name,
                    delete_src_after_copy,
                ),
                name=f"Copying {vrs_file}",
            )
            self._copy_tasks.add(t)
            t.add_done_callback(self._copy_tasks.discard)
        try:
            await asyncio.gather(*self._copy_tasks)
        except Exception:
            await self.cancel_copy()

    @log_exceptions
    async def cancel_copy(self):
        """Cancel the current copy operation."""
        if not self._copy_tasks:
            error_code = AriaError.VRS_PULL_NOT_STARTED
            raise AriaException(error_code, to_error_message(error_code))
        logger.debug("Cancelling import")
        for task in self._copy_tasks:
            if not task.done():
                task.cancel()
        try:
            # wait for cancellation to happen
            await asyncio.gather(*self._copy_tasks)
            logger.debug("Import cancelled")
        except asyncio.CancelledError:
            logger.debug("Copy cancelled")
        self._copy_tasks.clear()

    @log_exceptions
    def get_copy_progress(self) -> CopyStatus:
        """Get the copy progress."""
        if self._copy_tasks and any(not task.done() for task in self._copy_tasks):
            copied_bytes = 0
            for file_path in self._vrs_files_to_copy:
                local_path: Path = self._destination / file_path.name
                local_path_partial: Path = local_path.with_suffix(".partial")
                if local_path.exists():
                    copied_bytes += local_path.stat().st_size
                elif local_path_partial.exists():
                    copied_bytes += local_path_partial.stat().st_size
            self._copy_status.copied_bytes = copied_bytes

        return self._copy_status

    @log_exceptions
    async def _copy_vrs_and_metadata(
        self, device_vrs_path: Path, local_vrs_path: Path, delete_src: bool
    ):
        """Caopy a single vrs file from device to local along with the metadata file.
        The file is copied to a .partial file and then renamed.
        Optionally delete the file from device if delete_src is True."""
        async with self._semaphore:
            logger.debug(f"Start copying {device_vrs_path} to {local_vrs_path}")
            self._copy_status.current_files.append(device_vrs_path)

            async def __copy_file(device_file_path: Path, local_file_path: Path):
                """Copy a single file from device to local."""
                temp_dest_file: Path = local_file_path.with_suffix(".partial")
                await self._pull_file(device_file_path, temp_dest_file)
                temp_dest_file.rename(local_file_path)
                logger.debug(f"Done copying {device_file_path} to {local_file_path}")

            try:
                logger.debug(f"Copying {device_vrs_path} to {local_vrs_path}")
                await __copy_file(device_vrs_path, local_vrs_path)
                logger.debug(f"Copying metadata {device_vrs_path} to {local_vrs_path}")
                await __copy_file(
                    device_vrs_path.with_suffix(".vrs.json"),
                    local_vrs_path.with_suffix(".vrs.json"),
                )
                # This will save us file opening to create a thumbnail after the import
                # is complete.
                logger.debug(f"Copying thumbnail {device_vrs_path} to {local_vrs_path}")
                await self._copy_thumbnail_from_device_cache_to_local_file_cache(
                    device_vrs_path, local_vrs_path
                )
                self._copy_status.copied_files.append(local_vrs_path)
                if delete_src:
                    logger.debug(f"Deleting {device_vrs_path} from device")
                    try:
                        await self.delete_files([device_vrs_path])
                        self._copy_status.deleted_files.append(device_vrs_path)
                        logger.debug(f"Done deleting {device_vrs_path} from device")
                    except AriaException as e:
                        logger.exception(e)
                        # Swallow the exception and move on
                        logger.error(f"Failed to delete {device_vrs_path} from device")
            except asyncio.CancelledError:
                logger.error(f"Copy of {device_vrs_path} to {local_vrs_path} cancelled")
                raise
            except AriaException as e:
                logger.error(
                    f"Copy of {device_vrs_path} to {local_vrs_path} failed with {e.error_code}, {str(e)}"
                )
                self._copy_status.error = str(e)
                self._copy_status.error_files.append(device_vrs_path)
                raise
            finally:
                self._copy_status.current_files.remove(device_vrs_path)

    async def _copy_thumbnail_from_device_cache_to_local_file_cache(
        self, device_vrs_path: Path, local_vrs_path: Path
    ) -> None:
        """
        Copy thumbnail from device cache.
        If thumbnail is not found, then no action.
        """
        try:
            thumbnail_path_device_cache = await self.get_thumbnail_jpeg(
                device_vrs_path.name
            )
        except Exception as e:
            # Eat this exception as we don't want to fail the whole copy operation
            logger.error(e)
            logger.error(f"No thumbnail found for {device_vrs_path}")
            return

        # Copy the file from device cache to local
        file_manager = LocalFileManager.get_instance()
        thumbnail_path_local_cache = file_manager.cache.get_cache_dir(local_vrs_path)
        try:
            # Copy the file
            shutil.copy2(
                str(thumbnail_path_device_cache), str(thumbnail_path_local_cache)
            )
            logger.debug(
                f"File copied from {thumbnail_path_device_cache} to {thumbnail_path_local_cache}"
            )
        except Exception as e:
            logger.error(f"Error during thumnail copy: {e}")

    async def _get_total_size(self, vrs_files: List[Path]) -> int:
        """Get the total size of files in a list."""
        total_size: int = 0
        size_tasks = [
            self._adb_command(["shell", "stat", "-c", "%s", vrs_file])
            for vrs_file in vrs_files
        ]
        results = await asyncio.gather(*size_tasks, return_exceptions=True)
        for stdout, _ in results:
            total_size += int(stdout.strip())
        return total_size

    async def _adb_command(
        self,
        command: List[str],
        error_code: AriaError = AriaError.GENERIC_DEVICE_ERROR,
    ) -> Tuple[str, str]:
        """Helper to execute adb command asynchronously."""
        command = [str(self.adb_path_)] + [str(cmd) for cmd in command]
        logger.debug(f"Running command: {' '.join(command)}")
        process = await asyncio.create_subprocess_exec(
            *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout_str = b""
        stderr_str = b""
        try:
            stdout_str, stderr_str = await process.communicate()
        except asyncio.CancelledError:
            logger.debug(f"Killing {command}")
            process.terminate()
            await process.wait()
            logger.debug(f"Killed {command}")
        if process.returncode != 0:
            stdout_str = stdout_str.decode("UTF-8")
            stderr_str = stderr_str.decode("UTF-8")
            logger.error(f"{command} failed with {process.returncode}")
            logger.error(f"stdout: {stdout_str}")
            logger.error(f"stderr: {stderr_str}")
            try:
                await self.check_device_connected()
            except AriaException:
                error_code = AriaError.DEVICE_NOT_CONNECTED
            raise AriaException(error_code, to_error_message(error_code))
        return stdout_str, stderr_str
