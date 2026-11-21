from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

StatusPedido = Literal["pendente", "confirmado", "entregue", "cancelado"]


class PedidoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    data: datetime
    status: StatusPedido = "pendente"
    valor_total: Decimal = Field(..., ge=0, decimal_places=2)
    cliente_id: int = Field(..., gt=0)
    usuario_id: int = Field(..., gt=0)


class PedidoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    data: datetime | None = None
    status: StatusPedido | None = None
    valor_total: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    cliente_id: int | None = Field(default=None, gt=0)
    usuario_id: int | None = Field(default=None, gt=0)


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data: datetime
    status: StatusPedido
    valor_total: Decimal
    cliente_id: int
    cliente_nome: str
    usuario_id: int