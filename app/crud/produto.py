from sqlalchemy.orm import Session
from app.models.item_pedido import ItemPedido
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoUpdate
from sqlalchemy import select

def get_item_pedido(db: Session, itempedido_id: int) -> ItemPedido | None:
    return db.get(ItemPedido, itempedido_id)

def list_item_pedidos(db: Session, skip: int = 0, limit: int = 100) -> list[ItemPedido]:
    stmt = select(ItemPedido).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_item_pedido(db: Session, itempedido_in: ItemPedidoCreate) -> ItemPedido:
    itempedido = ItemPedido(**itempedido_in.model_dump())
    db.add(itempedido)
    db.commit()
    db.refresh(itempedido)
    return itempedido

def update_item_pedido(
    db: Session,
    itempedido: ItemPedido,
    itempedido_in: ItemPedidoUpdate,
) -> ItemPedido:
    update_data = itempedido_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(itempedido, field, value)
    db.commit()
    db.refresh(itempedido)
    return itempedido

def delete_item_pedido(db: Session, itempedido: ItemPedido) -> None:
    db.delete(itempedido)
    db.commit()

def get_item_pedido_by_pedido_id(db: Session, pedido_id: int) -> list[ItemPedido]:
    stmt = select(ItemPedido).where(ItemPedido.pedido_id == pedido_id)
    return list(db.scalars(stmt).all())

def get_item_pedido_by_produto_id(db: Session, produto_id: int) -> list[ItemPedido]:
    stmt = select(ItemPedido).where(ItemPedido.produto_id == produto_id)
    return list(db.scalars(stmt).all()) 
