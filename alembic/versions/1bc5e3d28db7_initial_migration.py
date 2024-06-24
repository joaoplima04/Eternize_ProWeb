"""Initial migration

Revision ID: 1bc5e3d28db7
Revises: a01cc1684ba5
Create Date: 2024-06-18 09:11:04.246231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc5e3d28db7'
down_revision: Union[str, None] = 'a01cc1684ba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('itemCarrinho', sa.Column('quantidade', sa.Integer(), nullable=False))
    op.drop_column('itemCarrinho', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('itemCarrinho', sa.Column('quantity', sa.INTEGER(), nullable=False))
    op.drop_column('itemCarrinho', 'quantidade')
    # ### end Alembic commands ###