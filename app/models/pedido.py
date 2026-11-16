from .base import Base
from sqlalchemy import String, CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from decimal import Decimal

class Pedido(Base):
    __tablename__ = "pedidos"

    __table_args__ = (
       
        CheckConstraint(
                    "valor_total >= 0",
                    name="ck_pedido_valor_total_nao_negativo"
                ),
        CheckConstraint(
                        "status IN ('pendente', 'confirmado', 'entregue', 'cancelado')",
                        name="ck_pedido_status_valido"
                        ),


    )


    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False
)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")
    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido", cascade="all, delete-orphan")