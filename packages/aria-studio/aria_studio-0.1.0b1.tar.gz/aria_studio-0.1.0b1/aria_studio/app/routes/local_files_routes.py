# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import asyncio
import logging
import os
from http import HTTPStatus
from pathlib import Path
from typing import List, Optional

from aria_studio.app.constants import KEY_FILE_NAME
from aria_studio.app.local.local_file_manager import LocalFileManager
from aria_studio.app.utils import login_required, run_and_forget
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DeleteLocalFilesRequest(BaseModel):
    files_to_delete: Optional[List[Path]] = None
    path_to_delete: Optional[Path] = None


class MediaModel(BaseModel):
    file_path: Path


class LocalFilesModel(BaseModel):
    sort_by: Optional[str] = None
    asc: bool = False
    page: int = 1
    per_page: int = 6
    path: str


router = APIRouter()


@login_required
@router.post("/delete")
def delete_files(request: DeleteLocalFilesRequest) -> JSONResponse:

    if not request.files_to_delete and not request.path_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="No files or folder is specified to delete.",
        )
    if request.path_to_delete:
        files_to_delete = list(request.path_to_delete.glob("*.vrs"))
    else:
        files_to_delete = request.files_to_delete

    try:
        file_manager = LocalFileManager.get_instance()
        file_manager.delete(files_to_delete)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": f"{len(files_to_delete)} file(s) deleted successfully."
            },
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@login_required
@router.post("/thumbnail_jpeg")
def serve_file(request: MediaModel):
    try:
        file_manager = LocalFileManager.get_instance()
        media_path = file_manager.get_thumbnail_jpeg(request.file_path)
        if media_path:
            return FileResponse(str(media_path))
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Thumbnail not found"
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/details")
def get_file_details(vrs_path: Path):
    # Return a JSON response with the metadata for the file at the given path
    try:
        file_manager = LocalFileManager.get_instance()
        return JSONResponse(
            status_code=HTTPStatus.OK, content=file_manager.get_metadata(vrs_path)
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/files")
def local_files(request: LocalFilesModel, requestObj: Request):
    if not Path(request.path).is_dir():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Directory not found"
        )
    try:
        file_manager = LocalFileManager.get_instance()
        output = file_manager.get_metadata_on_folder(Path(request.path))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    output = sorted(output, key=lambda x: x[KEY_FILE_NAME])
    # Return the paginated data in old paginated form which is what the frontend expects
    return {
        "count": len(output),  # Total number of items
        "next": None,  # URL for the next page
        "previous": None,  # URL for the previous page
        "results": output,  # Items for the current page
    }


@router.post("/view_vrs")
async def view_vrs(request: MediaModel):
    logger.debug(request)
    if not request.file_path:
        raise HTTPException(status_code=400, detail="Filename not provided")
    elif not request.file_path.is_file():
        raise HTTPException(
            status_code=400, etail=f"{request.file_path} file not found"
        )

    # During development we can have the local viewer_vrs script, since the pip package
    # is not installed
    viewer_vrs_cmd: List[str] = ["viewer_vrs"]
    if os.environ.get("LOCAL_VIEWER_VRS"):
        viewer_vrs_cmd = ["python", "-m", "aria_studio.utils.viewer_vrs"]

    command: List[str] = viewer_vrs_cmd + ["--vrs", str(request.file_path)]
    logger.debug(f"Running command: {' '.join(command)}")
    asyncio.create_task(run_and_forget(command), name="viewer_vrs")
