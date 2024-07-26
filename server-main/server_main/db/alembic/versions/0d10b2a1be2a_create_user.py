"""create user

Revision ID: 0d10b2a1be2a
Revises: e18ea1d6c8dd
Create Date: 2024-07-23 17:29:01.836236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d10b2a1be2a'
down_revision: Union[str, None] = 'e18ea1d6c8dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
