# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
from http import HTTPStatus
from pathlib import Path
from typing import Any, List, Mapping, Set

import jsons
from aria_studio.app.groups.group_manager import GroupManager
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class GroupResponse(BaseModel):
    name: str
    path_on_device: Path
    creation_time: int
    vrs_files: Set[Path]


class CreateGroupModel(BaseModel):
    name: str
    path: Path


class DeleteGroupsModel(BaseModel):
    names: List[str]


class AddFilesModel(BaseModel):
    name: str
    paths: List[Path]


class RemoveFilesModel(BaseModel):
    name: str
    paths: List[Path]


# TODO: Get logging working with FASTAPI
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list")
async def list_groups() -> JSONResponse:
    """
    Lists all the available groups
    """
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        groups = await group_manager.get_all()
        response: List[GroupResponse] = []
        for group in groups.values():
            response.append(
                GroupResponse(
                    name=group.name,
                    path_on_device=group.path_on_device,
                    creation_time=group.creation_time,
                    vrs_files=group.vrs_files,
                )
            )

        return response
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get("/get")
async def get_group(group_name: str) -> JSONResponse:
    """
    Get the details of a group
    """
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        group = await group_manager.get(group_name)
        if group is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"Group {group_name} not found"
            )
        return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(group))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post("/create")
async def create_group(grp: CreateGroupModel) -> JSONResponse:
    """
    Create a group
    """
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        group = await group_manager.create_group(grp.name, grp.path)
        return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(group))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post("/delete")
async def delete_groups(request: DeleteGroupsModel) -> JSONResponse:
    """
    Delete groups
    """
    try:
        if not request.names:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="No groups provided"
            )

        deleted_groups: List[str] = []

        for name in request.names:
            logger.debug(f"Deleting group {name}")
            try:
                group_manager: GroupManager = await GroupManager.get_instance()
                await group_manager.delete_group(name)
                deleted_groups.append(name)
            except Exception as e:
                logger.error(f"Error deleting group {name}: {e}")
        return deleted_groups
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post("/add_files")
async def add_files_to_group(inp: AddFilesModel) -> JSONResponse:
    """
    Add list of files to a group
    """
    logger.info(f"Adding {inp.paths} to group {inp.name}")
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        group = await group_manager.add_files(inp.name, inp.paths)
        return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(group))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post("/remove_files")
async def remove_files_from_group(inp: RemoveFilesModel) -> JSONResponse:
    """
    Remove a list of files from a group
    """
    logger.debug(f"Removing {inp.paths} from group {inp.name}")
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        group = await group_manager.remove_files(inp.name, inp.paths)
        return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(group))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get("/is_allowed")
async def is_allowed(group_name: str) -> JSONResponse:
    """
    Check if a group name is allowed to be used
    """
    result: Mapping[str, Any] = {}
    try:
        group_manager: GroupManager = await GroupManager.get_instance()
        result["allowed"] = not (await group_manager.exists(group_name))
        if result["allowed"]:
            result["detail"] = f"Group name '{group_name}' is allowed"
        else:
            result["detail"] = f"Group '{group_name}' already exists"
        return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(result))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
