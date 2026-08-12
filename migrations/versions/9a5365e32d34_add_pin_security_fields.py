"""add_pin_security_fields

Revision ID: 9a5365e32d34
Revises: 651eb9d5a565
Create Date: 2026-08-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a5365e32d34"
down_revision: Union[str, Sequence[str], None] = "651eb9d5a565"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "pin_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "pin_blocked_until",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "last_login_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "last_login_at")
    op.drop_column("users", "pin_blocked_until")
    op.drop_column("users", "pin_attempts")
