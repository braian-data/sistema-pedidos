from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

PerfilType = Literal["admin", "estoquista", "vendedor"]


class UsuarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    senha: str = Field(..., min_length=6)
    perfil: PerfilType

class UsuarioRegistro(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    senha: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=100)
    senha: str | None = Field(default=None, min_length=6)
    perfil: PerfilType | None = None


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    perfil: PerfilType

