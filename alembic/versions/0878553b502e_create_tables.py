"""Create tables

Revision ID: 0878553b502e
Revises: 7d3a6a5e93a3
Create Date: 2024-07-09 12:48:06.223148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0878553b502e'
down_revision: Union[str, None] = '7d3a6a5e93a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('telefone', sa.String(length=20), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('categoria', sa.Enum('PRATO_RASO', 'GUARDANAPO', 'TALHER', 'TACAS', 'TRILHOS_DE_MESA', 'SOUSPLAT', 'JOGO_AMERICANO', 'CHA_E_CAFE', 'PRATO_SOBREMESA', 'PORTA_GUARDANAPO', name='categoria'), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('quantidade_estoque', sa.Integer(), nullable=True),
    sa.Column('imagem', sa.String(length=255), nullable=True),
    sa.Column('cor', sa.String(length=100), nullable=True),
    sa.Column('estilo', sa.Enum('ELEGANTE', 'TROPICAL', 'FLORIDO', name='estilo'), nullable=True),
    sa.Column('publicado', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aluguel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cliente_cpf', sa.String(length=11), nullable=True),
    sa.Column('data_aluguel', sa.Date(), nullable=True),
    sa.Column('hora_inicial', sa.Time(), nullable=True),
    sa.Column('data_devolucao', sa.Date(), nullable=True),
    sa.Column('hora_final', sa.Time(), nullable=True),
    sa.Column('preco_total', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_cpf'], ['cliente.cpf'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itemCarrinho',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=True),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itemCarrinho_id'), 'itemCarrinho', ['id'], unique=False)
    op.create_table('entrega',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('aluguel_id', sa.Integer(), nullable=True),
    sa.Column('tipo_entrega', sa.String(), nullable=False),
    sa.Column('cep', sa.String(), nullable=True),
    sa.Column('endereco', sa.String(), nullable=True),
    sa.Column('bairro', sa.String(), nullable=True),
    sa.Column('cidade', sa.String(), nullable=True),
    sa.Column('numero', sa.String(), nullable=True),
    sa.Column('complemento', sa.String(), nullable=True),
    sa.Column('nome_destinatario', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['aluguel_id'], ['aluguel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entrega')
    op.drop_index(op.f('ix_itemCarrinho_id'), table_name='itemCarrinho')
    op.drop_table('itemCarrinho')
    op.drop_table('aluguel')
    op.drop_table('produto')
    op.drop_table('cliente')
    # ### end Alembic commands ###
