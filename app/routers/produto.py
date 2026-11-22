from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.produto import (
    get_produto,
    get_produto_by_nome,
    list_produtos,
    create_produto,
    update_produto,
    delete_produto,

)

from app.database import get_db
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
)

router = APIRouter(prefix="/produto", tags=["produtos"])

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto_in: ProdutoCreate,
    db: Session = Depends(get_db)
):
    if get_produto_by_nome(db, produto_in.nome):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    try:
        return create_produto(db, produto_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade: produto duplicado ou dados inválidos."
        )

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_produtos(db, skip=skip, limit=limit)

@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_in: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    produto = get_produto(db, produto_id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    try:
        return update_produto(db, produto_id, produto_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de integridade ao atualizar o produto."

        )

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
):
    produto = get_produto(db, produto_id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    delete_produto(db, produto)
