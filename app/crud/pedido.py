from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.crud.cliente import get_cliente
from app.crud.usuario import get_usuario
from app.exceptions import (
    EstoqueInsuficienteError,
    NaoEncontradoError,
    PedidoNaoRemovivelError,
    TransicaoStatusInvalidaError,
)
from app.models.estoque import Estoque
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.pedido import PedidoCreate

TRANSICOES: dict[str, set[str]] = {
    "pendente": {"confirmado", "cancelado"},
    "confirmado": {"entregue", "cancelado"},
    "entregue": set(),
    "cancelado": set(),
}


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
    if get_cliente(db, pedido_in.cliente_id) is None:
        raise NaoEncontradoError("Cliente não encontrado.")
    if get_usuario(db, pedido_in.usuario_id) is None:
        raise NaoEncontradoError("Usuário não encontrado.")

    pedido = Pedido(
        cliente_id=pedido_in.cliente_id,
        usuario_id=pedido_in.usuario_id,
        data=datetime.now(),
        status="pendente",
        valor_total=Decimal("0"),
    )
    total = Decimal("0")

    try:
        for item in pedido_in.itens:
            produto = db.get(Produto, item.produto_id)
            if produto is None:
                raise NaoEncontradoError(
                    f"Produto {item.produto_id} não encontrado."
                )

            estoque = db.scalar(
                select(Estoque)
                .where(Estoque.produto_id == item.produto_id)
                .with_for_update()
            )
            if estoque is None or estoque.quantidade < item.quantidade:
                raise EstoqueInsuficienteError(
                    f"Estoque insuficiente para o produto {item.produto_id}."
                )

            estoque.quantidade -= item.quantidade
            pedido.itens.append(
                ItemPedido(
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                    preco=produto.preco,
                )
            )
            total += produto.preco * item.quantidade

        pedido.valor_total = total
        db.add(pedido)
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(pedido)
    return pedido


def _devolver_estoque(db: Session, pedido: Pedido) -> None:
    for item in pedido.itens:
        estoque = db.scalar(
            select(Estoque)
            .where(Estoque.produto_id == item.produto_id)
            .with_for_update()
        )
        if estoque is None:
            db.add(Estoque(produto_id=item.produto_id, quantidade=item.quantidade))
        else:
            estoque.quantidade += item.quantidade


def update_pedido_status(db: Session, pedido: Pedido, novo_status: str) -> Pedido:
    if novo_status not in TRANSICOES[pedido.status]:
        raise TransicaoStatusInvalidaError(
            f"Não é possível mudar o pedido de '{pedido.status}' para '{novo_status}'."
        )

    try:
        if novo_status == "cancelado":
            _devolver_estoque(db, pedido)
        pedido.status = novo_status
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(pedido)
    return pedido


def delete_pedido(db: Session, pedido: Pedido) -> None:
    if pedido.status != "cancelado":
        raise PedidoNaoRemovivelError(
            "Só é possível apagar pedidos cancelados. Cancele o pedido antes."
        )
    db.delete(pedido)
    db.commit()