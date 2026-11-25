from app.models.usuario import Usuario
from app.security import hash_senha


def _criar_admin(db):
    db.add(
        Usuario(
            nome="Admin",
            email="admin@teste.com",
            senha=hash_senha("teste1234"),
            perfil="admin",
        )
    )
    db.commit()


def test_login_retorna_token(client, db):
    _criar_admin(db)

    r = client.post(
        "/auth/login",
        data={"username": "admin@teste.com", "password": "teste1234"},
    )

    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_com_senha_errada_retorna_401(client, db):
    _criar_admin(db)

    r = client.post(
        "/auth/login",
        data={"username": "admin@teste.com", "password": "errada"},
    )

    assert r.status_code == 401