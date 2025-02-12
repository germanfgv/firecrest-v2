# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from fastapi import (
    APIRouter,
)

# models
from lib.models import (
    ApiResponseError,
)


def create_router(
    prefix: str, tags: list = None, dependencies: list = None, responses: dict = None
):
    if responses is None:
        responses = {
            "4XX": {"model": ApiResponseError},
            "5XX": {"model": ApiResponseError},
        }
    return APIRouter(
        prefix=prefix, tags=tags, dependencies=dependencies, responses=responses
    )
