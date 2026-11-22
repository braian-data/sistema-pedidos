from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

StatusPedido = Literal["pendente", "confirmado", "entregue", "cancelado"]


class ItemPedidoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    produto_id: int = Field(..., gt=0)
    quantidade: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    cliente_id: int = Field(..., gt=0)
    usuario_id: int = Field(..., gt=0)
    itens: list[ItemPedidoEntrada] = Field(..., min_length=1)


class PedidoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: StatusPedido


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data: datetime
    status: StatusPedido
    valor_total: Decimal
    cliente_id: int
    cliente_nome: str
    usuario_id: int