"""atualiza constraint de perfil em usuarios

Revision ID: dd4d868a8808
Revises: eac497974b15
Create Date: 2026-11-21 04:00:11.224812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd4d868a8808'
down_revision: Union[str, Sequence[str], None] = 'eac497974b15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("ck_usuario_perfil_valido", "usuarios", type_="check")
    op.create_check_constraint(
        "ck_usuario_perfil_valido",
        "usuarios",
        "perfil IN ('admin', 'vendedor', 'gestor', 'estoquista')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_usuario_perfil_valido", "usuarios", type_="check")
    op.create_check_constraint(
        "ck_usuario_perfil_valido",
        "usuarios",
        "perfil IN ('gestor', 'funcionario')",
    )

