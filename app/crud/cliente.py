from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def get_cliente(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def list_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    stmt = select(Cliente).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_cliente(db: Session, cliente_in: ClienteCreate) -> Cliente:
    cliente = Cliente(**cliente_in.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update_cliente(
    db: Session,
    cliente: Cliente,
    cliente_in: ClienteUpdate,
) -> Cliente:
    update_data = cliente_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cliente, field, value)
    db.commit()
    db.refresh(cliente)
    return cliente


def delete_cliente(db: Session, cliente: Cliente) -> None:
    db.delete(cliente)
    db.commit()