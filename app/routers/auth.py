from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRegistro, UsuarioResponse
from app.crud.usuario import create_usuario, get_usuario_by_email
from app.database import get_db
from app.schemas.auth import Token
from app.security import criar_access_token, verificar_senha

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = get_usuario_by_email(db, form.username)

    if usuario is None or not verificar_senha(form.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_access_token(usuario.id, usuario.perfil)
    return Token(access_token=token)

@router.get("/me", response_model=UsuarioResponse)
def me(usuario: Usuario = Depends(get_current_user)):
    return usuario

@router.post(
    "/registro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def registro(dados: UsuarioRegistro, db: Session = Depends(get_db)):
    if get_usuario_by_email(db, dados.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    usuario_in = UsuarioCreate(**dados.model_dump(), perfil="vendedor")
    return create_usuario(db, usuario_in)
