# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import asyncio
import logging
from dataclasses import asdict
from http import HTTPStatus
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Set, Tuple

import jsons
from aria_studio.app.common.types import FeatureStatus
from aria_studio.app.constants import (
    CLOSED_LOOP_TRAJECTORY_FILE,
    KEY_MESSAGE,
    MESSAGE_MPS_PREPARING,
    SEMI_DENSE_POINTS_FILE,
)
from aria_studio.app.groups.group_manager import GroupManager
from aria_studio.app.mps.group_mps_request_manager import GroupMpsRequestManager
from aria_studio.app.mps.individual_mps_request_manager import (
    IndividualMpsRequestManager,
)
from aria_studio.app.utils import CliHttpHelper, login_required, run_and_forget
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from projectaria_tools.aria_mps_cli.cli_lib.types import MpsFeature, MpsRequest
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router: APIRouter = APIRouter()


class MpsIndividualModel(BaseModel):
    """
    Arguments for MPS single feature processing mode.
    See MPS CLI argument list for more details:
    https://facebookresearch.github.io/projectaria_tools/docs/ARK/mps/request_mps/mps_cli_guide#command-line-reference
    """

    features: Set[MpsFeature]
    input: List[Path]

    retry_failed: Optional[bool] = None
    force: Optional[bool] = None


class MpsMultiFeatureModel(BaseModel):
    """
    Arguments for MPS multi feature processing mode.
    See MPS CLI argument list for more details:
    https://facebookresearch.github.io/projectaria_tools/docs/ARK/mps/request_mps/mps_cli_guide#command-line-reference
    """

    groups: List[str]

    retry_failed: Optional[bool] = None
    force: Optional[bool] = None


class MultiRecordingRequestModel(BaseModel):
    force: bool = False
    suffix: str = ""
    retry_failed: bool = False
    output_dir: Path = ""


class IndividualStatusModel(BaseModel):
    vrs_paths: List[Path]


class IndividualRetryRequest(BaseModel):
    vrs_paths: List[Path] = Field(..., min_items=1)


class GroupHighLevelStatusModel(BaseModel):
    groups: List[str]


class ViewMpsRequest(BaseModel):
    vrs_path: Optional[Path] = None
    mps_path: Optional[Path] = None
    group_name: Optional[str] = None


def remove_none_values(d):
    """
    Recursively remove None values from a dictionary and empty lists.
    """

    if isinstance(d, dict):
        for key in list(d.keys()):
            if d[key] is None:
                del d[key]
            elif isinstance(d[key], list) and not d[key]:
                del d[key]
            else:
                remove_none_values(d[key])
    return d


@login_required
@router.get("/get-all-requests/")
async def get_all_requests() -> JSONResponse:
    requests: List[MpsRequest] = await CliHttpHelper.get().query_all_mps_requests()

    return {"requests": [remove_none_values(asdict(req)) for req in requests]}


@login_required
@router.post(
    "/view_mps",
    status_code=HTTPStatus.OK,
    summary="API to view MPS results along with the vrs file",
)
async def view_mps(request: ViewMpsRequest):
    """
    Execute a system call to open a file with viewer_mps.
    """

    async def get_group(group_name):
        group_manager: GroupManager = await GroupManager.get_instance()
        groups = await group_manager.get_all()
        if group_name not in groups:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Group not found"
            )
        return groups[group_name]

    if request.vrs_path:
        folder_path: str = request.vrs_path.parent / f"mps_{request.vrs_path.stem}_vrs"

        command = [
            "viewer_mps",
            "--vrs",
            str(request.vrs_path),
            "--mps_folder",
            str(folder_path),
        ]
    elif request.group_name:
        group = await get_group(request.group_name)

        closed_loop_trajectories = group.path_on_device.rglob(
            CLOSED_LOOP_TRAJECTORY_FILE
        )
        semi_dense_points = group.path_on_device.rglob(SEMI_DENSE_POINTS_FILE)
        command = ["viewer_mps"]
        command.append("--trajectory")
        for trj in closed_loop_trajectories:
            command.append(str(trj))
        command.append("--points")
        for sd in semi_dense_points:
            command.append(str(sd))
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No VRS files or group provided"
        )

    # We trigger the task and don't wait for the process to finish.
    asyncio.create_task(run_and_forget(command), name="viewer_mps")


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/single/request")
@router.post("/request-single/")
async def single_request(request: MpsIndividualModel):

    if not request.input:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No VRS files provided"
        )
    for vrs_path in request.input:
        if not vrs_path.is_file():
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="File not found"
            )
        try:
            individual_request_manager: IndividualMpsRequestManager = (
                await IndividualMpsRequestManager.get_instance()
            )
            await individual_request_manager.create_request(
                vrs_path, request.features, request.force, request.retry_failed
            )
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    return JSONResponse(
        status_code=HTTPStatus.ACCEPTED,
        content={KEY_MESSAGE: MESSAGE_MPS_PREPARING},
    )


@login_required
@router.post(
    "/individual/retry",
    status_code=status.HTTP_201_CREATED,
    summary="API to retry failed inidividual MPS feature requests",
)
async def single_retry(request: IndividualRetryRequest):
    retried: bool = False
    logger.debug(f"Individual retry request for {request}")
    for vrs_path in set(request.vrs_paths):
        individual_request_manager: IndividualMpsRequestManager = (
            await IndividualMpsRequestManager.get_instance()
        )
        retried = await individual_request_manager.retry_if_failed(vrs_path) or retried
    return status.HTTP_201_CREATED if retried else status.HTTP_204_NO_CONTENT


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/single/status")
@router.post("/check-processing-status/")
async def single_status(request: IndividualStatusModel):
    if not request.vrs_paths:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No VRS files provided"
        )
    status_per_file: Mapping[Path, Mapping[MpsFeature, FeatureStatus]] = {}
    for vrs_path in set(request.vrs_paths):
        if not vrs_path.is_file():
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"File not found {vrs_path}"
            )
        individual_request_manager: IndividualMpsRequestManager = (
            await IndividualMpsRequestManager.get_instance()
        )
        status_per_file[vrs_path] = await individual_request_manager.check_status(
            vrs_path
        )
    # TODO: T188502985 Remove old endpoint after the demo and fix the output schema
    # return status_per_file
    output_old_schema = {}
    for vrs_path, feature_status in status_per_file.items():
        last_request_time = 0
        for _, feature_status_item in feature_status.items():
            if feature_status_item and feature_status_item.creation_time:
                last_request_time = max(
                    last_request_time, feature_status_item.creation_time
                )

        output_old_schema[vrs_path] = {
            "features": feature_status,
            "last_request_date": last_request_time if last_request_time > 0 else None,
        }
    logger.debug(jsons.dump(output_old_schema, indent=2))
    return output_old_schema


@login_required
@router.post("/multi/request")
async def multi_request(request: MpsMultiFeatureModel):
    try:
        if not request.groups:
            raise Exception("No groups provided")

        group_mps_manager: GroupMpsRequestManager = (
            await GroupMpsRequestManager.get_instance()
        )
        for g in request.groups:
            await group_mps_manager.create_request(
                g, request.force, request.retry_failed
            )

        return JSONResponse(
            status_code=HTTPStatus.ACCEPTED,
            content={KEY_MESSAGE: MESSAGE_MPS_PREPARING},
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


def _get_high_level_status(
    status: Mapping[Path, Mapping[MpsFeature, FeatureStatus]]
) -> Tuple[Optional[str], Optional[int]]:
    logger.debug(f"Status is {status}")
    if not status:
        return None, None
    processing: bool = False
    for _, feature_feature_status in status.items():
        feature_status = feature_feature_status[MpsFeature.MULTI_SLAM]
        if feature_status.status == "Error":
            return "Failed", feature_status.error_code
        elif feature_status.status != "Success":
            processing = True
    s = "Processing" if processing else "Success"
    return s, None


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/multi/status_summary")
@router.post("/multi/high_level_status")
async def multi_status_summary(request: GroupHighLevelStatusModel):
    ## TODO: strongly type the response
    status_by_group: Dict[str, str] = {}
    if not request.groups:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No groups provided"
        )
    group_mps_manager: GroupMpsRequestManager = (
        await GroupMpsRequestManager.get_instance()
    )
    for group in request.groups:
        status = await group_mps_manager.check_status(group)
        status_by_group[group], err_code = _get_high_level_status(status)
        logger.info(f"Status for {group} is: {status_by_group[group]}")
    return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(status_by_group))


@login_required
@router.get("/multi/status")
async def multi_status(group: str, vrs_path: Optional[Path] = None):
    try:
        ## TODO: strongly type the response
        group_mps_manager: GroupMpsRequestManager = (
            await GroupMpsRequestManager.get_instance()
        )
        status_by_file = await group_mps_manager.check_status(group)
        output_old_schema = {}
        if status_by_file and vrs_path:
            if status_by_file and vrs_path not in status_by_file:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="File not found"
                )
            # TODO: T188502985 Remove old endpoint after the demo and fix the output schema
            # return status_per_file
            # return status.get(vrs_path, {})
            if vrs_path not in status_by_file:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="File not found"
                )
            feature_status = status_by_file[vrs_path]
            last_request_time = 0
            for _, f_status in feature_status.items():
                last_request_time = max(last_request_time, f_status.creation_time or 0)

            output_old_schema[vrs_path] = {
                "features": feature_status,
                "last_request_date": (
                    last_request_time if last_request_time > 0 else None
                ),
            }
        elif status_by_file:
            group_status, err_code = _get_high_level_status(status_by_file)
            last_request_time = 0
            for _, feature_status in status_by_file.items():
                for _, feature_status_item in feature_status.items():
                    last_request_time = max(
                        last_request_time, feature_status_item.creation_time or 0
                    )
            last_request_time = last_request_time if last_request_time > 0 else None
            group_manager: GroupManager = await GroupManager.get_instance()
            output_old_schema[group] = {
                "features": {
                    MpsFeature.MULTI_SLAM: FeatureStatus(
                        status=group_status,
                        # Error code is a string for more flexibility.
                        error_code=err_code,
                        creation_time=last_request_time,
                        output_path=(await group_manager.get(group)).path_on_device,
                    ),
                },
                "last_request_date": last_request_time,
            }

        return output_old_schema
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
