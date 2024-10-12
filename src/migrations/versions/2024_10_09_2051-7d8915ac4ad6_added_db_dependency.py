"""added db dependency

Revision ID: 7d8915ac4ad6
Revises: 76b3da704e03
Create Date: 2024-10-09 20:51:11.335587

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7d8915ac4ad6"
down_revision: Union[str, None] = "76b3da704e03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
