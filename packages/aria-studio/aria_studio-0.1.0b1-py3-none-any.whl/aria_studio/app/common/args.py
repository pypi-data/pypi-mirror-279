# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import argparse
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Args:
    """
    Class to hold the arguments passed in from command line
    """

    _args: Optional[argparse.Namespace] = None

    @classmethod
    def get_args(cls):
        """Get the arguments passed in from command line"""
        if cls._args is None:
            cls._args = _parse_arguments()
            logger.debug(f"args: {cls._args}")
        return cls._args


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-system-adb",
        action="store_true",
        help="Use adb binary that is already installed on the system. The default is to use the adb binary that comes with Aria Studio.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on",
    )
    parser.add_argument(
        "--no-browser",
        action="store_false",
        dest="browser",
        help="Do not open a browser window",
    )
    return parser.parse_args()
