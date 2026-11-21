from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.estoque import Estoque
from app.schemas.estoque import EstoqueCreate, EstoqueUpdate

def get_estoque(db: Session, estoque_id: int) -> Estoque | None:
    return db.get(Estoque, estoque_id)

def list_estoques(db: Session, skip: int = 0, limit: int = 100) -> list[Estoque]:
    stmt = select(Estoque).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_estoque(db: Session, estoque_in: EstoqueCreate) -> Estoque:
    estoque = Estoque(**estoque_in.model_dump())
    db.add(estoque)
    db.commit()
    db.refresh(estoque)
    return estoque

def update_estoque(
    db: Session,
    estoque: Estoque,
    estoque_in: EstoqueUpdate,
) -> Estoque:
    update_data = estoque_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(estoque, field, value)
    db.commit()
    db.refresh(estoque)
    return estoque

def delete_estoque(db: Session, estoque: Estoque) -> None:
    db.delete(estoque)
    db.commit()