import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

_password_hash = PasswordHash.recommended()


def hash_senha(senha: str) -> str:
    return _password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return _password_hash.verify(senha, senha_hash)


def criar_access_token(usuario_id: int, perfil: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(usuario_id), "perfil": perfil, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])