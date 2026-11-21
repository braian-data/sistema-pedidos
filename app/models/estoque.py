from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Estoque(Base):
    __tablename__ = "estoque"

    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_estoque_quantidade_nao_negativa"),
    )

    id: Mapped[int] = mapped_column("estoqueid", primary_key=True)
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.produtoid"),
        nullable=False,
        unique=True,
    )
    quantidade: Mapped[int] = mapped_column(nullable=False)

    produto: Mapped["Produto"] = relationship(back_populates="estoque")