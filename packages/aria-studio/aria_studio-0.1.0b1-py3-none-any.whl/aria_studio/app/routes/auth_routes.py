# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging

from aria_studio.app.constants import (
    KEY_LOGGED_IN,
    KEY_MESSAGE,
    KEY_USER,
    MESSAGE_LOGGED_IN_SUCCESS,
    MESSAGE_LOGGED_OUT_FAILED,
    MESSAGE_LOGGED_OUT_SUCCESS,
)
from aria_studio.app.groups.group_manager import GroupManager
from aria_studio.app.mps.group_mps_request_manager import GroupMpsRequestManager
from aria_studio.app.mps.individual_mps_request_manager import (
    IndividualMpsRequestManager,
)
from aria_studio.app.utils import CliAuthHelper, CliHttpHelper, login_required
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from projectaria_tools.aria_mps_cli.cli_lib.authentication import AuthenticationError
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str
    save_token: bool = False


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login")
async def login(login: LoginRequest) -> JSONResponse:
    try:
        await CliAuthHelper.get().login(
            username=login.username,
            password=login.password,
            save_token=login.save_token,
        )
        CliHttpHelper.get().set_auth_token(CliAuthHelper.get().auth_token)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={KEY_MESSAGE: MESSAGE_LOGGED_IN_SUCCESS},
        )
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/logout")
async def logout() -> JSONResponse:
    # We get the objects before logging out. To get the objects we need to be logged in.
    group_manager: GroupManager = await GroupManager.get_instance()
    individual_mps_request_manager: IndividualMpsRequestManager = (
        await IndividualMpsRequestManager.get_instance()
    )
    group_mps_request_manager: GroupMpsRequestManager = (
        await GroupMpsRequestManager.get_instance()
    )
    if await CliAuthHelper.get().logout():
        await group_manager.reset()
        await individual_mps_request_manager.reset()
        await group_mps_request_manager.reset()
        logger.info("Logged out successfully.")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={KEY_MESSAGE: MESSAGE_LOGGED_OUT_SUCCESS},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={KEY_MESSAGE: MESSAGE_LOGGED_OUT_FAILED},
        )


@router.get("/is-logged-in")
async def is_logged_in() -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={KEY_LOGGED_IN: CliAuthHelper.get().is_logged_in()},
    )


@login_required
@router.get("/current-user")
async def current_user() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={KEY_USER: CliAuthHelper.get().user}
    )
