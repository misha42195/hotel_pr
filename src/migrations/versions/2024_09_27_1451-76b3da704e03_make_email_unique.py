"""make email unique

Revision ID: 76b3da704e03
Revises: 21a3448f368c
Create Date: 2024-09-27 14:51:12.821721

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76b3da704e03"
down_revision: Union[str, None] = "21a3448f368c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
