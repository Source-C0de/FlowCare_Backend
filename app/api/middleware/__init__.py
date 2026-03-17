"""Exception handlers — maps domain exceptions to HTTP responses."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    ConflictException,
    DomainException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

def add_exception_handlers(app: FastAPI) -> None:
    """Register domain → HTTP exception mappers."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Filter out binary data from errors to avoid UnicodeDecodeError in jsonable_encoder
        errors = []
        for error in exc.errors():
            # Pydantic v2 might include the input value in the error
            # If it's bytes, we want to skip it or stringify it safely
            if "input" in error and isinstance(error["input"], bytes):
                error = error.copy()
                error["input"] = "<binary data>"
            errors.append(error)
            
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({"detail": errors}),
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=401, content={"detail": exc.message})

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(DomainException)
    async def domain_handler(request: Request, exc: DomainException):
        return JSONResponse(status_code=400, content={"detail": exc.message})
