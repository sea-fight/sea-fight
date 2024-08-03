"""create user

Revision ID: 70ecf292095e
Revises: 0d10b2a1be2a
Create Date: 2024-07-23 17:30:13.369545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70ecf292095e"
down_revision: Union[str, None] = "0d10b2a1be2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
