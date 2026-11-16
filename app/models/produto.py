from .base import Base
from sqlalchemy import String, CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal


class Produto(Base):
    __tablename__ = "produtos"

    __table_args__ = (
        CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_produto_nome_nao_vazio"
        ),
        CheckConstraint(
            "preco >= 0",
            name="ck_produto_preco_nao_negativo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    itens_pedido: Mapped[list["ItemPedido"]] = relationship(back_populates="produto")
    estoque: Mapped["Estoque"] = relationship(back_populates="produto")