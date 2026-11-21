from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    __table_args__ = (
        CheckConstraint("length(trim(nome)) > 0", name="ck_usuario_nome_nao_vazio"),
        CheckConstraint(
            "perfil IN ('admin', 'vendedor', 'gestor')",
            name="ck_usuario_perfil_valido",
        ),
    )

    id: Mapped[int] = mapped_column("usuarioid", primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(String(50), nullable=False)

    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="usuario")