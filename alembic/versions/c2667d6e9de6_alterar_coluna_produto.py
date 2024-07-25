"""Alterar coluna Produto

Revision ID: c2667d6e9de6
Revises: ee5100d7688d
Create Date: 2024-07-24 21:46:54.918871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2667d6e9de6'
down_revision: Union[str, None] = 'ee5100d7688d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
