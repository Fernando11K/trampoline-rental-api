# Comandos úteis

Referência rápida para terminal. Execute na **raiz do projeto**, com o **ambiente virtual ativado** e dependências instaladas (`pip install -r requirements.txt`).

> Em alguns shells use `flask --app app:create_app ...` (sem aspas simples em torno de `app:create_app`).

---

## Comando base (Flask-Migrate / Alembic)

```bash
flask --app 'app:create_app' <subcomando>
```

Exemplos de `<subcomando>`: `db upgrade`, `db current`, `db history`, `db migrate -m "mensagem"`, `db downgrade`.

Alternativa se `flask` não estiver no `PATH`:

```bash
python -m flask --app 'app:create_app' db upgrade
```

---

## Fluxo A — Do zero: sem banco e sem revisões em `migrations/versions/`

Quando **`migrations/versions/`** está vazia (sem `.py` de migração), por exemplo após clonar com `versions/` ignorada no Git.

```bash
flask --app 'app:create_app' db migrate -m "initial"
flask --app 'app:create_app' db upgrade
```

Opcional — conferir revisão aplicada:

```bash
flask --app 'app:create_app' db current
```

---

## Fluxo B — Já existem revisões em `migrations/versions/`

Quando já há ao menos um arquivo `.py` em `migrations/versions/` e você só precisa criar/atualizar o SQLite.

```bash
flask --app 'app:create_app' db upgrade
```

---

## Fluxo C — Arquivo de banco já existe (`database/db.trampoline`)

Sincronizar schema com as revisões (após `git pull`, troca de branch, etc.):

```bash
flask --app 'app:create_app' db upgrade
```

Inspecionar sem alterar:

```bash
flask --app 'app:create_app' db current
flask --app 'app:create_app' db history
```

---

## Refazer só o banco (mantém `migrations/versions/`)

Apaga o SQLite e reaplica todas as migrações até o `head`:

```bash
rm -f database/db.trampoline
flask --app 'app:create_app' db upgrade
```

**Windows (PowerShell):**

```powershell
Remove-Item -Force database/db.trampoline -ErrorAction SilentlyContinue
flask --app app:create_app db upgrade
```

---

## Refazer banco e migrações do zero

Apaga o SQLite **e** todas as revisões locais; gera uma migração `initial` nova a partir dos modelos atuais.

```bash
rm -f database/db.trampoline
rm -f migrations/versions/*.py
flask --app 'app:create_app' db migrate -m "initial"
flask --app 'app:create_app' db upgrade
```

**Windows (PowerShell):** apague manualmente os `.py` em `migrations\versions\` (exceto `__init__.py` se existir) ou use `Remove-Item migrations\versions\*.py`.

---

## Evoluir o schema (modelos em `models/` mudaram)

```bash
flask --app 'app:create_app' db migrate -m "descrição curta da mudança"
flask --app 'app:create_app' db upgrade
```

---

## Referência rápida — `db`

| Objetivo | Comando |
|----------|---------|
| Aplicar migrações pendentes | `flask --app 'app:create_app' db upgrade` |
| Revisão atual do banco | `flask --app 'app:create_app' db current` |
| Histórico de revisões | `flask --app 'app:create_app' db history` |
| Reverter a última migração (cuidado) | `flask --app 'app:create_app' db downgrade` |

---

## Executar a API

```bash
python app.py
```

Alternativa:

```bash
flask --app 'app:create_app' run --debug
```

A API costuma responder em **http://127.0.0.1:5000**. Documentação OpenAPI: **http://127.0.0.1:5000/openapi** (ou redirecionamento a partir de `/`).

---

## Banco desalinhado do Alembic (desenvolvimento)

Em geral: fazer backup de `database/db.trampoline`, apagar o arquivo e rodar **`db upgrade`** de novo. Se não houver revisões em `versions/`, use o **Fluxo A**.
