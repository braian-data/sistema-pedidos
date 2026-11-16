from .base import Base
from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    __table_args__ = (
        CheckConstraint(
            "quantidade > 0",
            name="quantidade_maior_que_zero"
        ),
        CheckConstraint(
            "valor_unitario >= 0",
            name="ck_item_pedido_valor_unitario_nao_negativo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(nullable=False)

    valor_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship(back_populates="itens_pedido")