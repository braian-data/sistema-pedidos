from fastapi import FastAPI
from fastapi import Depends, FastAPI
from app.dependencies import exigir_perfil, get_current_user
from app.routers.usuario import router as usuario_router
from app.routers.produto import router as produto_router
from app.routers.cliente import router as cliente_router
from app.routers.estoque import router as estoque_router
from app.routers.item_pedido import router as item_pedido_router
from app.routers.pedido import router as pedido_router
from app.routers.auth import router as auth_router


app = FastAPI(
    title="Sistema de Pedidos",
    description="API para gerenciamento de pedidos",
    version="1.0.0",
)

# Routers

app.include_router(auth_router)
app.include_router(usuario_router, dependencies=[Depends(exigir_perfil("admin"))])
app.include_router(cliente_router, dependencies=[Depends(exigir_perfil("admin", "gestor", "vendedor"))])
app.include_router(pedido_router, dependencies=[Depends(exigir_perfil("admin", "gestor", "vendedor"))])
app.include_router(produto_router, dependencies=[Depends(get_current_user)])
app.include_router(estoque_router, dependencies=[Depends(get_current_user)])
app.include_router(item_pedido_router, dependencies=[Depends(get_current_user)])



@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}
