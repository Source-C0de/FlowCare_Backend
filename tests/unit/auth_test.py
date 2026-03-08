from __future__ import annotations


import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.infra.core.security import hash_password
from app.main import app
from app.domain.entities.users import User

def _make_user(
    role: str = "CUSTOMER"
) -> MagicMock:
    u = MagicMock(spec=User)
    u.id = uuid.uuid4()
    u.email = "test@example.com"
    u.phone = "954343"
    u.hashed_password = hash_password("Test123")
    u.role_type = role
    u.is_active = True

    return u

@pytest.fixture
def client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )


@pytest.mark.asyncio
async def test_login_success_email(client: AsyncClient):
    user = _make_user()

    with(
        patch("app.application.use_cases.auth.UserRepositoryImpl.get_email_with_role", new_callable=AsyncMock, return_value=user)
    ):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "Test123"},
        )
    assert response.status_code == 200
    body = response.json()

