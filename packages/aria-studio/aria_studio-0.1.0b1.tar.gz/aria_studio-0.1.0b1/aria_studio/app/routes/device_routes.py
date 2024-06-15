# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
from pathlib import Path
from typing import Any, Final, List, Mapping, Optional

from aria_studio.app.constants import (
    KEY_DURATION,
    KEY_END_TIME,
    KEY_ERROR,
    KEY_FILE_NAME,
    KEY_FILE_SIZE,
    KEY_RECORDING_PROFILE,
    KEY_START_TIME,
    MESSAGE_DEVICE_NOT_CONNECTED,
    MESSAGE_FILE_NOT_FOUND,
)
from aria_studio.app.device.device_manager import (
    AriaError,
    AriaException,
    DeviceManager,
)
from aria_studio.app.utils import login_required
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

DEFAULT_PAGE = Query(1, ge=1)
DEFAULT_PER_PAGE = Query(6, ge=1)

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectedResponse(BaseModel):
    """Response from the connected endpoint"""

    connected: bool = Field(..., description="Is the device connected")


class DeviceStatusResponse(BaseModel):
    """Response from the status endpoint"""

    serial_number: str = Field(..., description="Serial number of the device")
    wifi_ssid: Optional[str] = Field(
        None, description="Wi-Fi SSID of the device if connected. None if not connected"
    )
    battery_level: int = Field(0, description="Battery level in percentage (0 to 100)")
    import_in_progress: bool = Field(..., description="Is an import in progress")


@login_required
@router.get(
    "/connected", status_code=status.HTTP_200_OK, summary="Is the device connected?"
)
async def connected():
    """Check if the device is connected"""
    try:
        device_manager = DeviceManager.get_instance()
        await device_manager.check_device_connected()
        return True
    except AriaException as e:
        logger.exception(e)
        return False


@login_required
@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    response_model=Optional[DeviceStatusResponse],
    summary="Get the device status (serial number, wifi ssid and battery level) of the device. If not connected to a device, return null",
)
async def device_status() -> Optional[DeviceStatusResponse]:
    """
    Retrieve the device status. If the device is not connected, return None.
    """
    try:
        device_manager = DeviceManager.get_instance()
        device_status = await device_manager.get_status()
        return DeviceStatusResponse(
            serial_number=device_status.serial_number,
            wifi_ssid=device_status.wifi_ssid,
            battery_level=device_status.battery_level,
            import_in_progress=device_status.import_in_progress,
        )
    except AriaException as e:
        if e.error_code == AriaError.DEVICE_NOT_CONNECTED:
            return None
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get device status {e}",
        )


class VrsFile(BaseModel):
    """Response from the list files api for each file"""

    vrs_filename: str = Field(..., description="The name of the vrs file")
    recording_profile: str = Field(
        ..., description="The recording profile of the vrs file"
    )
    start_time_epoch: int = Field(
        ...,
        description="The start time when the vrs file was recorded. Seconds since epoch",
    )
    end_time_epoch: int = Field(
        ...,
        description="The end time when the recording was stopped. Seconds since epoch",
    )
    file_size: int = Field(..., description="The size of the vrs file in bytes")


class ListFilesResponse(BaseModel):
    """Response from the list files api"""

    count: int = Field(..., description="The total number of files")
    next: Optional[str] = Field(None, description="Don't rely on this")
    previous: Optional[str] = Field(None, description="Don't rely on this")
    results: List[VrsFile] = Field(..., description="The list of vrs files")


class DeleteFilesRequest(BaseModel):
    """Delete files request"""

    files_to_delete: List[str] = Field([], description="List of file names to delete")


@login_required
@router.get(
    "/list-files",
    status_code=status.HTTP_200_OK,
    summary="List all the vrs files on the device and their metadata",
)
async def list_files(
    sort_by: Optional[str] = None,
    asc: bool = True,
    # ) -> Optional[ListFilesResponse]:
) -> JSONResponse:
    """
    Retrieve a list of files from the device, along with the necessary metadata.
    """
    files: List[Mapping[str, Any]] = []
    _RELEVANT_KEYS: Mapping[str, type] = {
        KEY_START_TIME: int,
        KEY_END_TIME: int,
        KEY_FILE_SIZE: int,
        KEY_RECORDING_PROFILE: str,
    }
    PROFILE_PREFIX: Final[str] = "profile"

    try:
        device_manager = DeviceManager.get_instance()
        vrs_files = await device_manager.list_vrs_files()
        for vrs_file in vrs_files:
            try:
                vrs_metadata: Mapping[str, Any] = await device_manager.get_metadata(
                    vrs_file
                )
                clean_metadata: Mapping[str, Any] = {
                    KEY_FILE_NAME: vrs_file.name,
                }
                for key, key_type in _RELEVANT_KEYS.items():
                    value = vrs_metadata[key]
                    # Check that the type is correct and fix it otherwise
                    if not isinstance(value, key_type):
                        value = key_type(value)
                    clean_metadata[key] = value
                files.append(clean_metadata)
            except AriaException as e:
                logger.error(f"Error retrieving metadata for {vrs_file}: {e}")
    except AriaException as e:
        if e.error_code == AriaError.DEVICE_NOT_CONNECTED:
            return {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}
        logger.error(f"Error retrieving list of files: {e}")
        logger.exception(e)

    if sort_by:

        def get_value(file):
            if sort_by == KEY_RECORDING_PROFILE:
                profile = file[KEY_RECORDING_PROFILE]
                return (
                    int(profile[len(PROFILE_PREFIX) :])
                    if profile.startswith(PROFILE_PREFIX)
                    else profile
                )

            elif sort_by == KEY_DURATION:
                return file[KEY_END_TIME] - file[KEY_START_TIME]

            elif sort_by in file:
                return file.get(sort_by)

            # by default sort by date
            return file[KEY_START_TIME]

        files = sorted(
            files,
            key=lambda x: get_value(x),
            reverse=asc,
        )
    return {"count": len(files), "results": files}


@login_required
@router.post(
    "/delete-files",
    status_code=status.HTTP_200_OK,
    summary="Delete vrs files, metadata and thumbnails associated with the list of vrs files",
)
async def delete_files(request: DeleteFilesRequest) -> None:
    """
    Delete specified files from the device.
    """
    try:
        device_manager = DeviceManager.get_instance()
        await device_manager.delete_files(request.files_to_delete)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class ImportFilesRequest(BaseModel):
    """Import files request"""

    destination_path: str = Field(..., description="The path to copy the file")
    files_to_import: List[str] = Field(
        ..., description="List of file names to import", min_items=1
    )
    delete: bool = Field(
        default=False, description="Delete files from device after import"
    )


class ImportStatusResponse(BaseModel):
    """Import status response"""

    current_files: List[str] = Field(
        ...,
        description="The current files being imported. This is all the files being imported concurrently",
    )
    copied_files: List[str] = Field(
        ..., description="The files that have already been copied"
    )
    deleted_files: List[str] = Field(
        ..., description="The files that have already been deleted"
    )
    total_files: int = Field(..., description="The number of files to import")
    copied_bytes: int = Field(..., description="The number of bytes copied")
    total_bytes: int = Field(..., description="The number of bytes to copy")
    error: Optional[str] = Field(None, description="The import error if any")
    error_files: List[str] = Field(
        [], description="The list of files that failed to import"
    )


class ImportCancelResponse(BaseModel):
    """Import cancel response"""

    success: bool = Field(..., description="Whether the import was cancelled")


@login_required
@router.post(
    "/import-files",
    status_code=status.HTTP_201_CREATED,
    response_model=ImportStatusResponse,
    summary="Initiate the import of vrs files from the device. If another import is in progress, exception is thrown.",
)
async def import_files(request: ImportFilesRequest):
    """Initiate the import of vrs files from the device."""
    try:
        device_manager = DeviceManager.get_instance()
        await device_manager.start_copy_vrs_files(
            request.files_to_import,
            destination=Path(request.destination_path),
            delete_src_after_copy=request.delete,
        )
        return await import_progress()
    except AriaException as e:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e)
        )
    except FileExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@login_required
@router.get(
    "/import-progress",
    status_code=status.HTTP_200_OK,
    response_model=ImportStatusResponse,
    summary="Get the import progress of vrs files from the device. If no import is in progress, return 400.",
)
async def import_progress():
    """Get the import progress of vrs files from the device. If no import is in progress, return 400."""
    try:
        device_manager = DeviceManager.get_instance()
        import_status = device_manager.get_copy_progress()
        return ImportStatusResponse(
            current_files=[f.name for f in import_status.current_files],
            copied_files=[f.name for f in import_status.copied_files],
            deleted_files=[f.name for f in import_status.deleted_files],
            total_files=import_status.total_files,
            copied_bytes=import_status.copied_bytes,
            total_bytes=import_status.total_bytes,
            error=import_status.error,
            error_files=[f.name for f in import_status.error_files],
        )
    except AriaException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@login_required
@router.post(
    "/cancel-import",
    status_code=status.HTTP_200_OK,
    response_model=ImportCancelResponse,
    summary="Cancel the ongoing import of vrs files from the device.",
)
async def cancel_import():
    """
    Cancel the ongoing import of vrs files from the device.
    """
    try:
        device_manager = DeviceManager.get_instance()
        await device_manager.cancel_copy()
        return ImportCancelResponse(success=True)
    except AriaException as e:
        if e.error_code == AriaError.VRS_PULL_NOT_STARTED:
            return ImportCancelResponse(success=False)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@login_required
@router.get(
    "/thumbnail_jpeg/{vrs_file}", summary="Get the jpeg thumbnail for a specified file"
)
async def thumbnail_jpeg(vrs_file: str):
    """
    Retrieve the thumbnail for a specified file.
    Args:
        vrs_file (str): The name of the file to retrieve the thumbnail for.
    Returns:
        FileResponse: The file response object containing the thumbnail.
    """
    try:
        device_manager = DeviceManager.get_instance()
        thumbnail = await device_manager.get_thumbnail_jpeg(vrs_file)
        return FileResponse(thumbnail)
    except AriaException as e:
        if e.error_code == AriaError.DEVICE_NOT_CONNECTED:
            return {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}
    except Exception as e:
        logger.exception(e)
        return {KEY_ERROR: MESSAGE_FILE_NOT_FOUND}


@login_required
@router.get(
    "/thumbnail_gif/{vrs_file}", summary="Get the gif thumbnail for a specified file"
)
async def thumbnail_gif(vrs_file: str):
    """
    Retrieve the gif thumbnail for a specified file.
    Args:
        vrs_file (str): The name of the file to retrieve the thumbnail for.
    Returns:
        FileResponse: The file response object containing the thumbnail.
    """
    try:
        device_manager = DeviceManager.get_instance()
        thumbnail = await device_manager.get_thumbnail_gif(vrs_file)

        return FileResponse(thumbnail)
    except AriaException as e:
        if e.error_code == AriaError.DEVICE_NOT_CONNECTED:
            return {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}
    except Exception as e:
        logger.exception(e)
        return {KEY_ERROR: MESSAGE_FILE_NOT_FOUND}
