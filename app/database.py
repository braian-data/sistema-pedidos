import os

from sqlalchemy import create_engine, URL, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, Session


def montar_url() -> URL:
    url = os.getenv("DATABASE_URL")
    if url:
        # Provedores entregam "postgres://" ou "postgresql://";
        # o SQLAlchemy precisa do nome do driver (psycopg) no prefixo.
        for prefixo in ("postgres://", "postgresql://"):
            if url.startswith(prefixo):
                url = "postgresql+psycopg://" + url[len(prefixo):]
                break
        return make_url(url)

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.environ["POSTGRES_DB"],
    )


DATABASE_URL = montar_url()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def testar_conexao():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Conexão com banco bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()