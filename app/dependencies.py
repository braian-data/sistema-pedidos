from collections.abc import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.crud.usuario import get_usuario
from app.database import get_db
from app.models.usuario import Usuario
from app.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decodificar_token(token)
        usuario_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise erro

    usuario = get_usuario(db, usuario_id)
    if usuario is None:
        raise erro

    return usuario


def exigir_perfil(*perfis: str) -> Callable[..., Usuario]:
    def verificador(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.perfil not in perfis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para esta ação.",
            )
        return usuario

    return verificador