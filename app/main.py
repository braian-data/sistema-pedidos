from fastapi import FastAPI

from app.routers.usuario import router as usuario_router

app = FastAPI(
    title="Sistema de Pedidos",
    description="API para gerenciamento de pedidos",
    version="1.0.0",
)

app.include_router(usuario_router)


@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}
