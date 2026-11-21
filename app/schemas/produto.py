from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProdutoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(..., min_length=1, max_length=100)
    preco: Decimal = Field(..., ge=0, decimal_places=2)


class ProdutoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str | None = Field(default=None, min_length=1, max_length=100)
    preco: Decimal | None = Field(default=None, ge=0, decimal_places=2)


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: Decimal