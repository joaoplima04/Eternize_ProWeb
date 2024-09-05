"""Alteração Aluguel

Revision ID: f35527cd517e
Revises: e4fb9b322007
Create Date: 2024-08-21 23:12:03.006911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f35527cd517e'
down_revision: Union[str, None] = 'e4fb9b322007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aluguel', sa.Column('data_pedido', sa.Date(), nullable=True))
    op.add_column('aluguel', sa.Column('objetivo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aluguel', 'objetivo')
    op.drop_column('aluguel', 'data_pedido')
    # ### end Alembic commands ###
