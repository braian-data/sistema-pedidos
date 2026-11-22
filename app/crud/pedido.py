from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate


def get_pedido(db: Session, pedido_id: int) -> Pedido | None:
    return db.get(Pedido, pedido_id)


def list_pedidos(db: Session, skip: int = 0, limit: int = 100) -> list[Pedido]:
    stmt = (
        select(Pedido)
        .options(joinedload(Pedido.cliente))
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def create_pedido(db: Session, pedido_in: PedidoCreate) -> Pedido:
    pedido = Pedido(**pedido_in.model_dump())
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def update_pedido(
    db: Session,
    pedido: Pedido,
    pedido_in: PedidoUpdate,
) -> Pedido:
    update_data = pedido_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pedido, field, value)
    db.commit()
    db.refresh(pedido)
    return pedido


def delete_pedido(db: Session, pedido: Pedido) -> None:
    db.delete(pedido)
    db.commit()