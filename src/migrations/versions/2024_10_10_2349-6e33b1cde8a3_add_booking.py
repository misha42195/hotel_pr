"""add booking

Revision ID: 6e33b1cde8a3
Revises: 7d8915ac4ad6
Create Date: 2024-10-10 23:49:06.556484

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6e33b1cde8a3"
down_revision: Union[str, None] = "7d8915ac4ad6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("price", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("bookings", "price")
