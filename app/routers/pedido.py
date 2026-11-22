from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.pedido import (
    create_pedido,
    delete_pedido,
    get_pedido,
    list_pedidos,
    update_pedido_status,
)
from app.database import get_db
from app.exceptions import NaoEncontradoError, RegraNegocioError
from app.schemas.pedido import (
    PedidoCreate,
    PedidoResponse,
    PedidoUpdate,
)

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    pedido_in: PedidoCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_pedido(db, pedido_in)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraNegocioError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro real do banco: {e.orig}",
        )


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_pedidos(db, skip=skip, limit=limit)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
):
    pedido = get_pedido(db, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    return pedido


@router.patch("/{pedido_id}", response_model=PedidoResponse)
def atualizar_pedido(
    pedido_id: int,
    pedido_in: PedidoUpdate,
    db: Session = Depends(get_db),
):
    pedido = get_pedido(db, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    try:
        return update_pedido_status(db, pedido, pedido_in.status)
    except RegraNegocioError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de integridade ao atualizar pedido.",
        )


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
):
    pedido = get_pedido(db, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    try:
        delete_pedido(db, pedido)
    except RegraNegocioError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))