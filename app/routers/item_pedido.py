from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.item_pedido import (
    create_item_pedido,
    delete_item_pedido,
    get_item_pedido,
    list_item_pedidos,
    update_item_pedido,
)
from app.database import get_db
from app.schemas.item_pedido import (
    ItemPedidoCreate,
    ItemPedidoResponse,
    ItemPedidoUpdate,
)

router = APIRouter(prefix="/itens-pedido", tags=["itens-pedido"])


@router.post(
    "/", response_model=ItemPedidoResponse, status_code=status.HTTP_201_CREATED
)
def criar_item_pedido(
    itempedido_in: ItemPedidoCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_item_pedido(db, itempedido_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro real do banco: {e.orig}",
        )


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


@router.patch("/{itempedido_id}", response_model=ItemPedidoResponse)
def atualizar_item_pedido(
    itempedido_id: int,
    itempedido_in: ItemPedidoUpdate,
    db: Session = Depends(get_db),
):
    itempedido = get_item_pedido(db, itempedido_id)

    if not itempedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    try:
        return update_item_pedido(db, itempedido, itempedido_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de integridade ao atualizar item do pedido.",
        )


@router.delete("/{itempedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item_pedido(
    itempedido_id: int,
    db: Session = Depends(get_db),
):
    itempedido = get_item_pedido(db, itempedido_id)

    if not itempedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    delete_item_pedido(db, itempedido)