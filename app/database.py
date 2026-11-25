
import os

from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker, Session

DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

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
