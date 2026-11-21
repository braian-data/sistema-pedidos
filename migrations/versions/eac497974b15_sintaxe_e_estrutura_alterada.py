"""Sintaxe e Estrutura alterada

Revision ID: eac497974b15
Revises: e9820f2534d6
Create Date: 2026-11-20 05:10:29.753697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac497974b15'
down_revision: Union[str, Sequence[str], None] = 'e9820f2534d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Remove FKs que referenciam PKs antigas ("id")
    op.drop_constraint('estoque_produto_id_fkey', 'estoque', type_='foreignkey')
    op.drop_constraint('pedidos_cliente_id_fkey', 'pedidos', type_='foreignkey')
    op.drop_constraint('pedidos_usuario_id_fkey', 'pedidos', type_='foreignkey')
    op.drop_constraint('itens_pedido_pedido_id_fkey', 'itens_pedido', type_='foreignkey')
    op.drop_constraint('itens_pedido_produto_id_fkey', 'itens_pedido', type_='foreignkey')

    # 2. Renomeia PKs para os nomes do DER
    op.alter_column(
        'clientes',
        'id',
        new_column_name='clienteid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'produtos',
        'id',
        new_column_name='produtoid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'usuarios',
        'id',
        new_column_name='usuarioid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'estoque',
        'id',
        new_column_name='estoqueid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'pedidos',
        'id',
        new_column_name='pedidoid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'itens_pedido',
        'id',
        new_column_name='itempedidoid',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )

    # 3. Renomeia valor_unitario -> preco em itens_pedido e ajusta perfil em usuarios
    op.alter_column(
        'itens_pedido',
        'valor_unitario',
        new_column_name='preco',
        existing_type=sa.Numeric(precision=10, scale=2),
        existing_nullable=False,
    )
    op.alter_column(
        'usuarios',
        'perfil',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )

    # 4. Recria FKs apontando para as novas PKs
    op.create_foreign_key(
        'estoque_produto_id_fkey',
        'estoque',
        'produtos',
        ['produto_id'],
        ['produtoid'],
    )
    op.create_foreign_key(
        'pedidos_cliente_id_fkey',
        'pedidos',
        'clientes',
        ['cliente_id'],
        ['clienteid'],
    )
    op.create_foreign_key(
        'pedidos_usuario_id_fkey',
        'pedidos',
        'usuarios',
        ['usuario_id'],
        ['usuarioid'],
    )
    op.create_foreign_key(
        'itens_pedido_pedido_id_fkey',
        'itens_pedido',
        'pedidos',
        ['pedido_id'],
        ['pedidoid'],
    )
    op.create_foreign_key(
        'itens_pedido_produto_id_fkey',
        'itens_pedido',
        'produtos',
        ['produto_id'],
        ['produtoid'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Remove FKs novas
    op.drop_constraint('estoque_produto_id_fkey', 'estoque', type_='foreignkey')
    op.drop_constraint('pedidos_cliente_id_fkey', 'pedidos', type_='foreignkey')
    op.drop_constraint('pedidos_usuario_id_fkey', 'pedidos', type_='foreignkey')
    op.drop_constraint('itens_pedido_pedido_id_fkey', 'itens_pedido', type_='foreignkey')
    op.drop_constraint('itens_pedido_produto_id_fkey', 'itens_pedido', type_='foreignkey')

    # 2. Reverte ajustes de colunas
    op.alter_column(
        'usuarios',
        'perfil',
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        'itens_pedido',
        'preco',
        new_column_name='valor_unitario',
        existing_type=sa.Numeric(precision=10, scale=2),
        existing_nullable=False,
    )

    # 3. Reverte nomes das PKs para "id"
    op.alter_column(
        'itens_pedido',
        'itempedidoid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'pedidos',
        'pedidoid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'estoque',
        'estoqueid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'usuarios',
        'usuarioid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'produtos',
        'produtoid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        'clientes',
        'clienteid',
        new_column_name='id',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )

    # 4. Recria FKs originais apontando para "id"
    op.create_foreign_key(
        'estoque_produto_id_fkey',
        'estoque',
        'produtos',
        ['produto_id'],
        ['id'],
    )
    op.create_foreign_key(
        'pedidos_cliente_id_fkey',
        'pedidos',
        'clientes',
        ['cliente_id'],
        ['id'],
    )
    op.create_foreign_key(
        'pedidos_usuario_id_fkey',
        'pedidos',
        'usuarios',
        ['usuario_id'],
        ['id'],
    )
    op.create_foreign_key(
        'itens_pedido_pedido_id_fkey',
        'itens_pedido',
        'pedidos',
        ['pedido_id'],
        ['id'],
    )
    op.create_foreign_key(
        'itens_pedido_produto_id_fkey',
        'itens_pedido',
        'produtos',
        ['produto_id'],
        ['id'],
    )