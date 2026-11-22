class NaoEncontradoError(Exception):
    """Entidade referenciada não existe (vira 404)."""


class RegraNegocioError(Exception):
    """Violação de regra de negócio (vira 409)."""


class EstoqueInsuficienteError(RegraNegocioError):
    """Produto sem estoque para a quantidade pedida."""


class TransicaoStatusInvalidaError(RegraNegocioError):
    """Mudança de status não permitida."""


class PedidoNaoRemovivelError(RegraNegocioError):
    """Pedido não pode ser apagado no status atual."""