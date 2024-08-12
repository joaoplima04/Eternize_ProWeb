"""Cliente superuser

Revision ID: e4fb9b322007
Revises: c2667d6e9de6
Create Date: 2024-08-10 11:46:10.447032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4fb9b322007'
down_revision: Union[str, None] = 'c2667d6e9de6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cliente', sa.Column('superuser', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cliente', 'superuser')
    # ### end Alembic commands ###
