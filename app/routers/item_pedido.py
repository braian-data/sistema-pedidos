from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.item_pedido import get_item_pedido, list_item_pedidos
from app.database import get_db
from app.schemas.item_pedido import ItemPedidoResponse

router = APIRouter(prefix="/itens-pedido", tags=["itens-pedido"])


@router.get("/", response_model=list[ItemPedidoResponse])
def listar_item_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_item_pedidos(db, skip=skip, limit=limit)


@router.get("/{itempedido_id}", response_model=ItemPedidoResponse)
def obter_item_pedido(
    itempedido_id: int,
    db: Session = Depends(get_db),
):
    itempedido = get_item_pedido(db, itempedido_id)

    if not itempedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    return itempedido