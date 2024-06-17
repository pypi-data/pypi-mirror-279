from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError, ValidationException
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Union
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
        headers=exc.headers if hasattr(exc, "headers") else None,
    )


async def handle_request_exception(request: Request,
                                   exc: Union[RequestValidationError, ValidationException]) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.errors()},
    )
