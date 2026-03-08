import pytest
from httpx import ASGITransport, AsyncClient
import uuid
import sys
from app.main import app
from app.domain.entities.users import User
from app.infra.core.security import hash_password

import asyncio

from unittest.mock import AsyncMock, patch
from tests.unit.auth_test import _make_user

async def main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        user = _make_user()
        with patch("app.application.use_cases.auth.UserRepositoryImpl.get_email_with_role", new_callable=AsyncMock, return_value=user):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "test@example.com", "password": "Test123"},
            )
            print("Response text:", response.text)
            print("Code:", response.status_code)

asyncio.run(main())
