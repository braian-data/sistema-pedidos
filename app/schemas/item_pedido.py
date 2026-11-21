from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    pedido_id: int = Field(..., gt=0)
    produto_id: int = Field(..., gt=0)
    preco: Decimal = Field(..., gt=0, decimal_places=2)
    quantidade: int = Field(..., gt=0)


class ItemPedidoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    pedido_id: int | None = Field(default=None, gt=0)
    produto_id: int | None = Field(default=None, gt=0)
    preco: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    quantidade: int | None = Field(default=None, gt=0)


class ItemPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    itempedidoid: int
    pedido_id: int
    produto_id: int
    preco: Decimal
    quantidade: int