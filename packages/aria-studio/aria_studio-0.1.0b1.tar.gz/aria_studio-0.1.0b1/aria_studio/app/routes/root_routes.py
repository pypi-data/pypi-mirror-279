# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/docs", response_class=RedirectResponse)
async def docs(self):
    """Redirect to the FastAPI documentation."""
    return RedirectResponse(url="/docs")


frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"


@router.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve the React app."""
    try:
        if full_path.startswith("api"):
            return {"detail": "Not Found"}
        file_path = frontend_path / full_path
        if not file_path.is_file():
            file_path = frontend_path / "index.html"
        return FileResponse(str(file_path))
    except FileNotFoundError:
        raise HTTPException(status_code=404)


# Serve static files
router.mount(
    "/static", StaticFiles(directory=str(frontend_path / "static")), name="static"
)
