"""Change mesage text string(300) field to Text

Revision ID: 43d7289cdf26
Revises: 5f073a048fb7
Create Date: 2024-01-07 14:29:23.171437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43d7289cdf26'
down_revision: Union[str, None] = '5f073a048fb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
