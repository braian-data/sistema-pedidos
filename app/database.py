from sqlalchemy import create_engine, URL, text
import os

DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_HOST = os.getenv("DB_HOST", "db")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=5432,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)

def testar_conexao():
    try:
        with engine.connect() as conexao:
            resultado = conexao.execute(text("SELECT 1"))
            return resultado.scalar()
    except Exception as {e}:
        print(f"Ocorreu um erro na conexão com o db: {e}")
        
