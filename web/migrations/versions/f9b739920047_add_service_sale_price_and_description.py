"""add service sale price and description

Revision ID: f9b739920047
Revises: d959ce40a293
Create Date: 2026-08-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f9b739920047"
down_revision: Union[str, Sequence[str], None] = "d959ce40a293"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # description bazada allaqachon mavjud.
    # sale_price oldingi urinishda ham qo'shilgan bo'lishi mumkin.
    # Shuning uchun faqat ustun mavjudligini tekshiramiz.

    bind = op.get_bind()

    inspector = sa.inspect(bind)
    columns = {
        column["name"]
        for column in inspector.get_columns("services")
    }

    if "sale_price" not in columns:
        op.add_column(
            "services",
            sa.Column(
                "sale_price",
                sa.Numeric(18, 6),
                nullable=False,
                server_default="0",
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()

    inspector = sa.inspect(bind)
    columns = {
        column["name"]
        for column in inspector.get_columns("services")
    }

    if "sale_price" in columns:
        op.drop_column("services", "sale_price")
