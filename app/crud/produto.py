from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def get_produto(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)


def get_produto_by_nome(db: Session, nome: str) -> Produto | None:
    stmt = select(Produto).where(Produto.nome == nome)
    return db.scalars(stmt).first()


def list_produtos(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    stmt = select(Produto).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_produto(db: Session, produto_in: ProdutoCreate) -> Produto:
    produto = Produto(**produto_in.model_dump())
    db.add(produto)
    try:
        db.commit()
        db.refresh(produto)
        return produto
    except IntegrityError:
        db.rollback()
        raise


def update_produto(
    db: Session,
    produto: Produto,
    produto_in: ProdutoUpdate,
) -> Produto:
    update_data = produto_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(produto, field, value)
    try:
        db.commit()
        db.refresh(produto)
        return produto
    except IntegrityError:
        db.rollback()
        raise


def delete_produto(db: Session, produto: Produto) -> None:
    db.delete(produto)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
