from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(..., min_length=1, max_length=100)
    telefone: str = Field(..., min_length=1, max_length=20)
    endereco: str = Field(..., min_length=1, max_length=200)


class ClienteUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str | None = Field(default=None, min_length=1, max_length=100)
    telefone: str | None = Field(default=None, min_length=1, max_length=20)
    endereco: str | None = Field(default=None, min_length=1, max_length=200)


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    endereco: str