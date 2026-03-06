"""make id_image_path nullable

Revision ID: 7f2e2a9c9c3b
Revises: 3626ba6bbe0f
Create Date: 2026-03-06 21:00:00.000000

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7f2e2a9c9c3b"
down_revision = "3626ba6bbe0f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "id_image_path",
        existing_type=sa.String(length=500),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "id_image_path",
        existing_type=sa.String(length=500),
        nullable=False,
    )

