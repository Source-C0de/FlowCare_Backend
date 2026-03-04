from fastapi import Request
from fastapi.responses import JSONResponse
# from app.domain.exceptions import (
#     DomainException, NotFoundException, UnauthorizedException,
#     ConflictException, ValidationException
# )


def add_exception_handlers(app):
    # @app.exception_handler(NotFoundException)
    # async def not_found_handler(request: Request, exc: NotFoundException):
    #     return JSONResponse(status_code=404, content={"detail": str(exc)})

    # @app.exception_handler(ConflictException)
    # async def conflict_handler(request: Request, exc: ConflictException):
    #     return JSONResponse(status_code=409, content={"detail": str(exc)})

    # @app.exception_handler(UnauthorizedException)
    # async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    #     return JSONResponse(status_code=403, content={"detail": str(exc)})

    # @app.exception_handler(ValidationException)
    # async def validation_handler(request: Request, exc: ValidationException):
    #     return JSONResponse(status_code=422, content={"detail": str(exc)})

    # @app.exception_handler(DomainException)
    # async def domain_handler(request: Request, exc: DomainException):
    #     return JSONResponse(status_code=400, content={"detail": str(exc)})
    return ""
