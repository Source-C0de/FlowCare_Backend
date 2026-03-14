"""Domain-level exceptions.

These are framework-agnostic. The API layer maps them to HTTP responses.
This follows the Dependency Rule — domain never imports FastAPI.
"""


class DomainException(Exception):
    """Base for all domain errors."""

    def __init__(self, message: str = "A domain error occurred"):
        self.message = message
        super().__init__(message)


class NotFoundException(DomainException):
    """Entity was not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class ConflictException(DomainException):
    """Duplicate / conflict error."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message)


class UnauthorizedException(DomainException):
    """Authentication failure."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)


class ForbiddenException(DomainException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message)


class ValidationException(DomainException):
    """Business-rule validation failure."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)
