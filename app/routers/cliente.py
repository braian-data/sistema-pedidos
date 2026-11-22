from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.cliente import (
    create_cliente,
    get_cliente,
    get_cliente_by_nome,  # 1. Import necessário para o POST
    list_clientes,
    update_cliente,
    delete_cliente,
)
from app.database import get_db
from app.schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(
    cliente_in: ClienteCreate,
    db: Session = Depends(get_db),
):
    if get_cliente_by_nome(db, cliente_in.nome):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cliente já cadastrado.",
        )

    try:
        return create_cliente(db, cliente_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro real do banco: {e.orig}",
        )


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(  # 2. Renomeado para não entrar em loop infinito com list_clientes
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_clientes(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    cliente = get_cliente(db, cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente_in: ClienteUpdate,
    db: Session = Depends(get_db),
):
    cliente = get_cliente(db, cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    try:
        return update_cliente(db, cliente, cliente_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de integridade ao atualizar o cliente",
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)  # 3. Corrigido de 209 para 204
def remover_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    cliente = get_cliente(db, cliente_id)  # 4. Corrigido de get_usuario para get_cliente

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )

    delete_cliente(db, cliente)
