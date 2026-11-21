from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    __table_args__ = (
        CheckConstraint("valor_total >= 0", name="ck_pedido_valor_total_nao_negativo"),
        CheckConstraint(
            "status IN ('pendente', 'confirmado', 'entregue', 'cancelado')",
            name="ck_pedido_status_valido",
        ),
    )

    id: Mapped[int] = mapped_column("pedidoid", primary_key=True)
    data: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.clienteid"), nullable=False
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuarioid"), nullable=False
    )

    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")
    usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")
    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )

    @property
    def cliente_nome(self) -> str:
        return self.cliente.nome