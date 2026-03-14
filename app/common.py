"""
Common imports used across the application to reduce boilerplate.
WARNING: Only put external libraries (FastAPI, Pydantic, SQLAlchemy) or 
very basic internal utilities here to avoid Circular Import errors.
"""

# Typing
from typing import Optional, Any, Callable, List

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Cookie

# Pydantic
from pydantic import BaseModel, Field

# SQLAlchemy
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

# Common app modules (Only core dependencies - NO models/schemas to prevent circular loops)
from app.infrastructure.database.session import AsyncSessionLocal, get_db
from app.domain.exceptions import DomainException


#Response
from fastapi.responses import JSONResponse


#Datetime
from datetime import datetime


#Dataclass
from dataclasses import dataclass


#Pagination
from app.infrastructure.utils.pagination import PaginationRequest,pagination_params

__all__ = [
    "Optional", "Any", "Callable", "List",
    "APIRouter", "Depends", "HTTPException", "status", "Request", "Response", "Cookie",
    "BaseModel", "Field",
    "select", "func", "update", "delete", "AsyncSession",
    "AsyncSessionLocal", "get_db", "DomainException"
]
