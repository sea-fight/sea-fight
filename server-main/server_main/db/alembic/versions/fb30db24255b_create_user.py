"""create user

Revision ID: fb30db24255b
Revises: dcc01f36bae8
Create Date: 2024-07-23 15:46:03.314076

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fb30db24255b"
down_revision: Union[str, None] = "dcc01f36bae8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
