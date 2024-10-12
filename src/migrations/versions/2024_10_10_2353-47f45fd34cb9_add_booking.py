"""add booking

Revision ID: 47f45fd34cb9
Revises: 6e33b1cde8a3
Create Date: 2024-10-10 23:53:10.688717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "47f45fd34cb9"
down_revision: Union[str, None] = "6e33b1cde8a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
