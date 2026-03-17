"""Logout-user use case."""

from __future__ import annotations

from app.infrastructure.security.token_utils import hash_token


class LogoutUserUseCase:
    """Handles token revocation on logout."""

    async def execute(self, refresh_token: str | None) -> None:
        if refresh_token is None:
            return
        _token_hash = hash_token(refresh_token)
        # TODO: persist revocation to a token blacklist table



__all__ = [
    "LogoutUserUseCase"
]
