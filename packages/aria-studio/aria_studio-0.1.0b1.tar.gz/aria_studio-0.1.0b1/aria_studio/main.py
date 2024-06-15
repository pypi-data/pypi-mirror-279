# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging

import uvicorn
from aria_studio.app.common.args import Args
from aria_studio.app.constants import LOCALHOST, LOGGING_PATH, LOGGING_YML_PATH
from aria_studio.app.routes import (
    auth_routes,
    device_routes,
    explorer_routes,
    group_routes,
    local_files_routes,
    mps_routes,
    root_routes,
)
from aria_studio.app.utils import lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(title="Aria Studio", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# adding it so that users can't use public ip to access aria studio on other devices.
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", LOCALHOST])

app.include_router(device_routes.router, prefix="/device")
app.include_router(local_files_routes.router, prefix="/local")
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(mps_routes.router, prefix="/mps")
app.include_router(group_routes.router, prefix="/group")
app.include_router(explorer_routes.router, prefix="/explorer")
app.include_router(root_routes.router, prefix="")


def run():
    ## Create log directory so that loggint can be initialized for uvicorn
    LOGGING_PATH.mkdir(parents=True, exist_ok=True)
    args = Args.get_args()
    uvicorn.run(
        "aria_studio.main:app",
        host=LOCALHOST,
        port=args.port,
        reload=False,
        log_config=str(LOGGING_YML_PATH),
        workers=1,
    )


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, RuntimeError):
        print("Shutting down...")
