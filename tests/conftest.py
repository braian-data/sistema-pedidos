import os

from dotenv import load_dotenv

# Precisa vir ANTES de qualquer import de "app": o database.py lê o ambiente na importação.
load_dotenv()
os.environ["POSTGRES_DB"] = "pedidos_test"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5434"
os.environ.setdefault("SECRET_KEY", "chave-so-para-teste")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import SessionLocal, engine
from app.main import app
from app.models.base import Base


@pytest.fixture(scope="session", autouse=True)
def criar_schema():
    # Trava de segurança: nunca recriar tabelas fora do banco de teste.
    assert engine.url.database.endswith("_test"), "Testes só podem rodar em banco *_test"
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture(autouse=True)
def limpar_tabelas():
    yield
    with engine.begin() as conn:
        tabelas = ", ".join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
        conn.execute(text(f"TRUNCATE {tabelas} RESTART IDENTITY CASCADE"))


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    return TestClient(app)