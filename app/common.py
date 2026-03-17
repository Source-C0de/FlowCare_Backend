"""
Common imports used across the application to reduce boilerplate.
WARNING: Only put external libraries (FastAPI, Pydantic, SQLAlchemy) or 
very basic internal utilities here to avoid Circular Import errors.
"""
"""
Common imports used across the application to reduce boilerplate.

Guidelines:
- Only include stable external libraries or very basic internal utilities.
- Avoid importing models, schemas, or business services here to prevent circular imports.
"""

# =========================
# Python Standard Library
# =========================
from typing import Optional, Any, Callable, List, Dict
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from dataclasses import dataclass
import uuid
from uuid import UUID


# =========================
# FastAPI
# =========================
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Response,
    Cookie,
    File,
    UploadFile
)

from fastapi.responses import (
    JSONResponse,
    StreamingResponse
)

# =========================
# Pydantic
# =========================
from pydantic import BaseModel, Field

# =========================
# SQLAlchemy
# =========================
from sqlalchemy import (
    select,
    func,
    update,
    delete,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UUID as SQL_UUID,
    Index,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
 
# =========================
# Application Core
# =========================
from app.infrastructure.database.session import (
    AsyncSessionLocal,
    get_db
)
from app.domain.exceptions import DomainException

# =========================
# Pagination Utilities
# =========================
from app.infrastructure.utils.pagination import (
    PaginationRequest,
    pagination_params
)

# =========================
# Exported Symbols
# =========================
__all__ = [

    # typing
    "Optional",
    "Any",
    "Callable",
    "List",
    "Dict",

    # datetime / uuid
    "datetime",
    "timezone",
    "UUID",
    "uuid",

    # dataclass
    "dataclass",

    # fastapi
    "APIRouter",
    "Depends",
    "HTTPException",
    "status",
    "Request",
    "Response",
    "Cookie",

    # responses
    "JSONResponse",
    "StreamingResponse",

    # pydantic
    "BaseModel",
    "Field",

    # sqlalchemy core & types
    "Column",
    "Integer",
    "String",
    "Boolean",
    "DateTime",
    "ForeignKey",
    "relationship",
    "Text",
    "JSONB",
    "JSON",
    "SQL_UUID",
    "hybrid_property",
    "Index",
    "Table",
    "select",
    "func",
    "update",
    "delete",
    "AsyncSession",

    # database
    "AsyncSessionLocal",
    "get_db",

    # exceptions
    "DomainException",

    # pagination
    "PaginationRequest",
    "pagination_params",

    # file
    "File",
    "UploadFile",

    # abc
    "ABC",
    "abstractmethod"
]