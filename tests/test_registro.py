from app.crud.usuario import get_usuario_by_email

NOVO = {"nome": "Ana", "email": "ana@teste.com", "senha": "senha1234"}


def test_registro_cria_vendedor_com_senha_em_hash(client, db):
    r = client.post("/auth/registro", json=NOVO)

    assert r.status_code == 201
    assert r.json()["perfil"] == "vendedor"
    assert "senha" not in r.json()

    usuario = get_usuario_by_email(db, "ana@teste.com")
    assert usuario.senha != "senha1234"


def test_registro_com_email_repetido_retorna_409(client):
    client.post("/auth/registro", json=NOVO)

    r = client.post("/auth/registro", json=NOVO)

    assert r.status_code == 409


def test_registro_recusa_campo_perfil(client, db):
    r = client.post("/auth/registro", json={**NOVO, "perfil": "admin"})

    assert r.status_code == 422
    assert get_usuario_by_email(db, "ana@teste.com") is None


def test_login_com_conta_recem_criada(client):
    client.post("/auth/registro", json=NOVO)

    r = client.post(
        "/auth/login",
        data={"username": "ana@teste.com", "password": "senha1234"},
    )

    assert r.status_code == 200
    assert "access_token" in r.json()