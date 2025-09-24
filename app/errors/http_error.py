from fastapi import Request, status
from fastapi.responses import JSONResponse

class CustomHTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def http_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, CustomHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    # Optionally, handle other exceptions or re-raise
    raise exc
