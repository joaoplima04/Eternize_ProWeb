"""Alterar coluna cpf na tabela cliente

Revision ID: ee5100d7688d
Revises: cbc2553261dd
Create Date: 2024-07-23 20:13:54.546047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee5100d7688d'
down_revision: Union[str, None] = 'cbc2553261dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
