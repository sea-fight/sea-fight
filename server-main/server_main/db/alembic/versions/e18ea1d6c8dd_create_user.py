"""create user

Revision ID: e18ea1d6c8dd
Revises: fb30db24255b
Create Date: 2024-07-23 17:28:35.754512

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e18ea1d6c8dd"
down_revision: Union[str, None] = "fb30db24255b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
