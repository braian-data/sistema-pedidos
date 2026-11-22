from fastapi import FastAPI

from app.routers.usuario import router as usuario_router
from app.routers.produto import router as produto_router
from app.routers.cliente import router as cliente_router
from app.routers.estoque import router as estoque_router
from app.routers.item_pedido import router as item_pedido_router
from app.routers.pedido import router as pedido_router

app = FastAPI(
    title="Sistema de Pedidos",
    description="API para gerenciamento de pedidos",
    version="1.0.0",
)

# Routers
app.include_router(usuario_router)
app.include_router(produto_router)
app.include_router(cliente_router)
app.include_router(estoque_router)
app.include_router(pedido_router)
app.include_router(item_pedido_router)


@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}
