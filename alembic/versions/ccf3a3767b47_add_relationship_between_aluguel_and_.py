"""Add relationship between Aluguel and ItemCarrinho

Revision ID: ccf3a3767b47
Revises: 0878553b502e
Create Date: 2024-07-09 12:52:40.783575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccf3a3767b47'
down_revision = '0878553b502e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adicionar coluna aluguel_id à tabela itemCarrinho
    op.add_column('itemCarrinho', sa.Column('aluguel_id', sa.Integer(), nullable=True))
    
    # Criar uma nova chave estrangeira para a tabela itemCarrinho
    op.create_foreign_key(
        'fk_itemCarrinho_aluguel', 'itemCarrinho', 'aluguel', ['aluguel_id'], ['id']
    )

def downgrade() -> None:
    # Remover a chave estrangeira
    op.drop_constraint('fk_itemCarrinho_aluguel', 'itemCarrinho', type_='foreignkey')
    
    # Remover a coluna aluguel_id
    op.drop_column('itemCarrinho', 'aluguel_id')
