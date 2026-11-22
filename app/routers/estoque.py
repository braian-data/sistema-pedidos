from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.estoque import (
    create_estoque,
    delete_estoque,
    get_estoque,
    get_estoque_by_produto_id,
    list_estoques,
    update_estoque,
)
from app.database import get_db
from app.schemas.estoque import (
    EstoqueCreate,
    EstoqueResponse,
    EstoqueUpdate,
)

router = APIRouter(prefix="/estoques", tags=["estoques"])


@router.post("/", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
def criar_estoque(
    estoque_in: EstoqueCreate,
    db: Session = Depends(get_db),
):
    if get_estoque_by_produto_id(db, estoque_in.produto_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe estoque cadastrado para este produto.",
        )

    try:
        return create_estoque(db, estoque_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro real do banco: {e.orig}",
        )


@router.get("/", response_model=list[EstoqueResponse])
def listar_estoques(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_estoques(db, skip=skip, limit=limit)


@router.get("/{estoque_id}", response_model=EstoqueResponse)
def obter_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
):
    estoque = get_estoque(db, estoque_id)

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado.",
        )

    return estoque


@router.patch("/{estoque_id}", response_model=EstoqueResponse)
def atualizar_estoque(
    estoque_id: int,
    estoque_in: EstoqueUpdate,
    db: Session = Depends(get_db),
):
    estoque = get_estoque(db, estoque_id)

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado.",
        )

    try:
        return update_estoque(db, estoque, estoque_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de integridade ao atualizar estoque.",
        )


@router.delete("/{estoque_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
):
    estoque = get_estoque(db, estoque_id)

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado.",
        )

    delete_estoque(db, estoque)