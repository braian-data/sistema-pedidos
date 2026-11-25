# Sistema de Pedidos e Estoque

API REST para gerenciar clientes, produtos, estoque e pedidos, com autenticação JWT e controle de acesso por perfil.

**Demo no ar:** https://pedidos-api-36i0.onrender.com/docs

> Hospedada no plano gratuito do Render. Se a API estiver parada, a primeira requisição pode levar cerca de 1 minuto para acordar.

## Como testar a demo

1. Abra o link acima e use `POST /auth/registro` para criar uma conta (nome, e-mail e senha com no mínimo 6 caracteres). Toda conta criada por aqui tem perfil `vendedor`.
2. Clique em **Authorize** (cadeado), preencha `username` com o **e-mail** e `password` com a senha. Deixe `client_id` e `client_secret` vazios.
3. Use as rotas de clientes, produtos, estoque e pedidos.

Sinta-se à vontade para criar quantas contas quiser. O banco da demo é gratuito e pode ser apagado periodicamente.

## Tecnologias

- Python 3.13, FastAPI, Pydantic
- SQLAlchemy 2.x (driver psycopg 3) e Alembic (migrations)
- PostgreSQL 17
- Autenticação com JWT (HS256, expira em 30 min) e hash de senha com argon2 (pwdlib)
- Pytest para testes, rodando em banco separado
- Docker e Docker Compose
- Deploy no Render

## Regras de negócio

- O total do pedido é calculado no servidor, nunca enviado pelo cliente.
- A baixa de estoque acontece na mesma transação do pedido. Se algo falhar, tudo sofre rollback.
- Cancelar um pedido devolve os itens ao estoque.
- As mudanças de status do pedido seguem transições válidas, com resposta `404` (não encontrado) ou `409` (transição inválida).

## Autenticação e permissões

- `401`: não autenticado (sem token ou token inválido).
- `403`: autenticado, mas sem permissão para a ação.

| Rota | Quem acessa |
|---|---|
| `/auth/registro`, `/auth/login` | Público |
| `/auth/me` | Qualquer usuário logado |
| `/clientes`, `/pedidos` | admin, gestor, vendedor |
| `/produtos`, `/estoque`, `/itens-pedido` | Qualquer usuário logado |
| `/usuarios` | Somente admin |

O cadastro público nunca aceita o campo `perfil`: o servidor sempre cria o usuário como `vendedor`, o que evita escalada de privilégio.

## Rodando localmente

Pré-requisitos: Docker e Docker Compose.

```bash
cp .env.example .env        # preencha os valores (use uma SECRET_KEY própria)
docker compose up -d
docker compose exec api alembic upgrade head
```

A API fica em http://localhost:8000/docs.

### Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL única de conexão (usada em produção). Se existir, as variáveis `POSTGRES_*` não são necessárias |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Conexão local por variáveis separadas |
| `DB_HOST`, `DB_PORT` | Host e porta do banco (padrão `db` e `5432`) |
| `SECRET_KEY` | Chave de assinatura do JWT. Gere uma nova para produção |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token (padrão `30`) |

## Testes

Os testes usam um banco separado (`pedidos_test`) e se recusam a rodar em qualquer banco que não termine em `_test`.

```bash
docker compose up -d db
pytest -q
```

## Deploy

O deploy é automático: o merge na `main` dispara o build no Render. O container aplica as migrations (`alembic upgrade head`) antes de iniciar a API, então um banco vazio vira o schema completo sem passo manual. A configuração (`DATABASE_URL`, `SECRET_KEY`) fica nas variáveis de ambiente do Render, nunca no repositório.

## Limitações conhecidas

- Plano gratuito: a API dorme após 15 minutos sem uso e o banco expira em 30 dias, sem backup.
- Não há limite de cadastros nem de tentativas de login.

## Próximos passos

- Seed automático do primeiro admin
- Endpoint de health check e configuração de CORS
- Rate limit no login e no cadastro
- Validação de formato de e-mail
- Logs estruturados e backup do banco