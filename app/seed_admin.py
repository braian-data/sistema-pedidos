import os

from sqlalchemy.orm import Session

from app.crud.usuario import get_usuario_by_email
from app.database import engine
from app.models.usuario import Usuario
from app.security import hash_senha


def main() -> None:
    email = os.getenv("ADMIN_EMAIL")
    senha = os.getenv("ADMIN_PASSWORD")
    nome = os.getenv("ADMIN_NOME", "Administrador")

    if not email or not senha:
        print("ADMIN_EMAIL/ADMIN_PASSWORD nao definidos: seed ignorado.")
        return

    with Session(engine) as db:
        if get_usuario_by_email(db, email):
            print("Admin ja existe: nada a fazer.")
            return
        db.add(
            Usuario(nome=nome, email=email, senha=hash_senha(senha), perfil="admin")
        )
        db.commit()
        print("Admin criado.")


if __name__ == "__main__":
    main()
