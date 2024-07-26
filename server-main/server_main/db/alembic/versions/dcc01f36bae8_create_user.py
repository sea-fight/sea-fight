"""create user

Revision ID: dcc01f36bae8
Revises: e404592615a0
Create Date: 2024-07-23 15:09:12.500950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcc01f36bae8'
down_revision: Union[str, None] = 'e404592615a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
