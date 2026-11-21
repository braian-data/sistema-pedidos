from pydantic import BaseModel, ConfigDict, Field


class EstoqueCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    produto_id: int = Field(..., gt=0)
    quantidade: int = Field(..., ge=0)


class EstoqueUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    produto_id: int | None = Field(default=None, gt=0)
    quantidade: int | None = Field(default=None, ge=0)


class EstoqueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    quantidade: int