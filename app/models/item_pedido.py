from decimal import Decimal
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    __table_args__ = (
        CheckConstraint("preco > 0", name="ck_item_pedido_preco_positivo"),
        CheckConstraint("quantidade > 0", name="ck_item_pedido_quantidade_positiva"),
    )

    itempedidoid: Mapped[int] = mapped_column(primary_key=True)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.pedidoid"), nullable=False
    )
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.produtoid"), nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship(back_populates="itens_pedido")