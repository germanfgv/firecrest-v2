# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

import os
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# models
from lib.models import (
    ApiResponseMeta,
    ApiResponseError,
)

# helpers
from lib.helpers.api_auth_helper import ApiAuthHelper


HEADERS_META_PREFIX_KEY = "F7T"


def _response_headers_meta(request: Request = None, exc: Exception = None) -> dict:
    meta_model = ApiResponseMeta.build_http_meta(
        app_version=os.getenv("APP_VERSION") or "local",
        auth=ApiAuthHelper.get_auth() if ApiAuthHelper.is_authenticated() else None,
    )
    headers_meta = {
        f"{HEADERS_META_PREFIX_KEY}-Timestamp": str(meta_model.timestamp),
        f"{HEADERS_META_PREFIX_KEY}-AppVersion": meta_model.app_version,
    }
    if meta_model.has_auth():
        headers_meta[f"{HEADERS_META_PREFIX_KEY}-AuthUsername"] = (
            meta_model.get_auth_username()
        )
    if exc and hasattr(exc, "headers"):
        if exc.headers:
            headers_meta = {**headers_meta, **exc.headers}
    return headers_meta


async def meta_headers_handler(request: Request, call_next):
    headers = _response_headers_meta(request=request)
    response = await call_next(request)
    response.headers.update(headers)
    return response


def response_error_handler(exc: Exception, request: Request = None) -> JSONResponse:
    error_model, error_status_code = ApiResponseError.build_http_error_from_exception(
        exc=exc
    )
    error_model.user = ApiAuthHelper.get_auth_username()

    headers = _response_headers_meta(request=request, exc=exc)
    return JSONResponse(
        status_code=error_status_code,
        content=jsonable_encoder(error_model),
        headers=headers,
    )
