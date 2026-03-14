"""Token hashing utilities."""

from __future__ import annotations

import hashlib


def hash_token(token: str) -> str:
    """SHA-256 hash for DB storage of refresh tokens."""
    return hashlib.sha256(token.encode()).hexdigest()
