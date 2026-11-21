"""cria tabelas iniciais

Revision ID: e9820f2534d6
Revises:
Create Date: 2026-11-17 16:06:56.490162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9820f2534d6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'clientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=False),
        sa.Column('endereco', sa.String(length=200), nullable=False),
        sa.CheckConstraint('length(trim(nome)) > 0', name='ck_cliente_nome_nao_vazio'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'produtos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('preco', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.CheckConstraint('length(trim(nome)) > 0', name='ck_produto_nome_nao_vazio'),
        sa.CheckConstraint('preco >= 0', name='ck_produto_preco_nao_negativo'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('senha', sa.String(length=255), nullable=False),
        sa.Column('perfil', sa.String(length=100), nullable=False),
        sa.CheckConstraint(
            "perfil IN ('gestor', 'funcionario')",
            name='ck_usuario_perfil_valido',
        ),
        sa.CheckConstraint('length(trim(nome)) > 0', name='ck_usuario_nome_nao_vazio'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'estoque',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.CheckConstraint(
            'quantidade >= 0',
            name='ck_estoque_quantidade_nao_negativa',
        ),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('produto_id'),
    )
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('valor_total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "status IN ('pendente', 'confirmado', 'entregue', 'cancelado')",
            name='ck_pedido_status_valido',
        ),
        sa.CheckConstraint(
            'valor_total >= 0',
            name='ck_pedido_valor_total_nao_negativo',
        ),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id']),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'itens_pedido',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column(
            'valor_unitario',
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.CheckConstraint(
            'quantidade > 0',
            name='ck_item_pedido_quantidade_maior_que_zero',
        ),
        sa.CheckConstraint(
            'valor_unitario >= 0',
            name='ck_item_pedido_valor_unitario_nao_negativo',
        ),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('itens_pedido')
    op.drop_table('pedidos')
    op.drop_table('estoque')
    op.drop_table('usuarios')
    op.drop_table('produtos')
    op.drop_table('clientes')