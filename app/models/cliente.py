from app.models.pedido import Pedido

from .base import Base
from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cliente(Base):
    __tablename__ = "clientes"

    __table_args__ = (
        CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_cliente_nome_nao_vazio"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    endereco: Mapped[str] = mapped_column(String(200), nullable=False)

    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")
 
