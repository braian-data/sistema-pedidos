from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.database import get_db


def get_usuario(db: Session, usuario_id: int) -> Usuario | None:
    return db.get(Usuario, usuario_id)

def list_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    stmt = select(Usuario).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_usuario(db: Session, usuario_in: UsuarioCreate) -> Usuario:
    usuario = Usuario(**usuario_in.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def update_usuario(
    db: Session,
    usuario: Usuario,
    usuario_in: UsuarioUpdate,
) -> Usuario:
    update_data = usuario_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_usuario(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()

def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.email == email)
    return db.scalars(stmt).first()
