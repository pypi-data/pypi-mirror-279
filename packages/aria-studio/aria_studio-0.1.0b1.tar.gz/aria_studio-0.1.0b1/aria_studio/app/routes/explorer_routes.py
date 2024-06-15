# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
import os
from datetime import datetime
from http import HTTPStatus
from json import JSONDecodeError
from pathlib import Path
from typing import List

from aria_studio.app.constants import (
    DEFAULT_PATH,
    KEY_LAST_MODIFIED,
    KEY_MESSAGE,
    KEY_NAME,
    KEY_PATH,
    MESSAGE_DIRECTORY_ALREADY_EXISTS,
    MESSAGE_DIRECTORY_NOT_FOUND,
    MESSAGE_INVALID_JSON,
    PERMISSION_DENIED,
)
from aria_studio.app.utils import login_required
from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


class ExplorerResponse(BaseModel):
    """Response from the explorer endpoint"""

    current_path: str = Field(..., description="The current path")
    files: List[dict] = Field(..., description="List of files")
    directories: List[dict] = Field(..., description="List of directories")


@login_required
@router.post("/file-explorer", response_model=ExplorerResponse)
async def file_explorer(request: Request) -> ExplorerResponse:
    """
    List all files and directories in the specified directory.

    Args:
        path (str): The path to the directory.
    """
    try:
        data = await request.json()
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=MESSAGE_INVALID_JSON
        )

    path = data.get(KEY_PATH, DEFAULT_PATH) or DEFAULT_PATH

    if not Path(path).exists():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=MESSAGE_DIRECTORY_NOT_FOUND
        )

    files = []
    directories = []

    try:
        items = list(Path(path).iterdir())
    except PermissionError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=PERMISSION_DENIED)

    for item in items:
        if item.name.startswith("."):  # Skip hidden files
            continue
        modified_time = datetime.fromtimestamp(os.path.getmtime(item)).isoformat()
        if item.is_file():
            files.append({KEY_NAME: item.name, KEY_LAST_MODIFIED: modified_time})
        elif item.is_dir():
            directories.append({KEY_NAME: item.name, KEY_LAST_MODIFIED: modified_time})

    files = sorted(files, key=lambda x: x[KEY_LAST_MODIFIED], reverse=True)
    directories = sorted(directories, key=lambda x: x[KEY_LAST_MODIFIED], reverse=True)
    return ExplorerResponse(
        current_path=str(path), files=files, directories=directories
    )


@login_required
@router.post("/create-new-directory", status_code=status.HTTP_201_CREATED)
async def create_new_directory(request: Request) -> JSONResponse:
    """
    Create a new directory with the specified name in the specified path.

    Args:
        path (str): The path where the new directory will be created.
        name (str): The name of the new directory.

    Returns:
        JSONResponse: The response containing a success message if the directory was created successfully.
    """
    try:
        data = await request.json()
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=MESSAGE_INVALID_JSON
        )

    if KEY_PATH not in data or KEY_NAME not in data:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Missing parameter: 'path' and 'name' are required",
        )
    path = data.get(KEY_PATH)
    name = data.get(KEY_NAME)
    directory_path = Path(path) / name
    if directory_path.exists():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MESSAGE_DIRECTORY_ALREADY_EXISTS,
        )

    try:
        directory_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=PERMISSION_DENIED)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={KEY_MESSAGE: f"Directory '{name}' created successfully at '{path}'"},
    )
