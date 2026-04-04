# Trampoline Rental API

API REST em **Flask** para **registro e consulta** de aluguéis de trampolins (criação e listagem/consulta por id). A documentação interativa segue **OpenAPI 3** (Swagger / Redoc / RapiDoc) via `flask-openapi3`. O armazenamento é **SQLite** em arquivo local, com esquema gerenciado por **Flask-Migrate** (Alembic).

## Pré-requisitos

- **Python** 3.10 ou superior (recomendado 3.11+)
- **pip** (geralmente incluído com Python)
- **Git** (para clonar o repositório)

## Instalação e configuração do ambiente local

### 1. Clonar o repositório

```bash
git clone <url-do-repositório>
cd trampoline-rental-api
```

### 2. Criar e ativar um ambiente virtual

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

As principais dependências estão listadas em `requirements.txt` (Flask, Flask-SQLAlchemy, flask-openapi3, Pydantic, Flask-Migrate, Flask-Cors).

Em seguida configure **SQLite e Alembic** na próxima seção, **Banco de dados e migrações**. Os mesmos comandos também estão reunidos em **[`docs/comandos-uteis.md`](docs/comandos-uteis.md)** para consulta rápida.

---

## Banco de dados e migrações (Flask-Migrate / Alembic)

O SQLite fica em **`database/db.trampoline`** (veja `config.py`). A pasta **`database/`** é criada quando a aplicação sobe ou quando o Alembic grava o banco, se ainda não existir.

As **revisões** (scripts que criam/alteram tabelas) ficam em **`migrations/versions/*.py`**. O restante da pasta **`migrations/`** (`env.py`, `script.py.mako`, `alembic.ini`, etc.) é a configuração do Alembic.

**Comando base** (sempre na raiz do projeto, com o venv ativado):

```bash
flask --app 'app:create_app' <subcomando>
```

> Em alguns terminais use `flask --app app:create_app ...` (sem aspas simples).

---

### A) Configurar do zero: sem banco e sem revisões em `migrations/versions/`

Use quando você **acabou de clonar**, apagou o SQLite ou a pasta **`migrations/versions/`** está **vazia** (sem arquivos `.py` de migração).

1. Conclua os passos de **venv** e **`pip install`** (seção *Instalação*).
2. **Gere** a primeira revisão a partir dos modelos atuais:

   ```bash
   flask --app 'app:create_app' db migrate -m "initial"
   ```

3. **Aplique** no SQLite (cria `database/db.trampoline` e as tabelas, se necessário):

   ```bash
   flask --app 'app:create_app' db upgrade
   ```

4. (Opcional) Confira a revisão aplicada:

   ```bash
   flask --app 'app:create_app' db current
   ```

Se quiser **descartar** um banco antigo e refazer só o arquivo (mantendo suas revisões em `versions/`), apague `database/db.trampoline` e rode de novo **`db upgrade`**.

---

### B) Já existem revisões em `migrations/versions/` (ex.: arquivos `.py` no disco ou versionados no Git)

Use quando a pasta **`migrations/versions/`** já contém ao menos uma revisão e você quer só **materializar** o schema no SQLite.

1. Conclua **venv** e **`pip install`**.
2. Rode:

   ```bash
   flask --app 'app:create_app' db upgrade
   ```

Isso cria ou atualiza **`database/db.trampoline`** até a revisão **head**. Não é necessário rodar **`db migrate`** nesse caso, a menos que você tenha **mudado os modelos** e precise de uma revisão nova (veja a seção *Evoluir o schema*).

---

### C) O arquivo de banco já existe (`database/db.trampoline`)

Use quando você **já rodou a API** antes, copiou o `.sqlite` de outro lugar ou acabou de fazer o fluxo **A** ou **B**.

1. Com **venv** e dependências instaladas, rode:

   ```bash
   flask --app 'app:create_app' db upgrade
   ```

2. O Alembic compara o banco com as revisões em **`migrations/versions/`**:
   - se o banco já está na mesma revisão que o código, o comando costuma **não alterar** nada;
   - se há revisões **novas** (por exemplo após um `git pull` que trouxe `.py` em `versions/`), só o que falta é aplicado.

3. Para inspecionar sem alterar:

   ```bash
   flask --app 'app:create_app' db current
   flask --app 'app:create_app' db history
   ```

Se o banco estiver **desalinhado** do histórico Alembic (erro ao subir ou ao rodar `upgrade`), o caminho mais simples em desenvolvimento costuma ser: backup do arquivo, apagar **`database/db.trampoline`** e rodar de novo **`db upgrade`** (ou refazer o fluxo **A** se não houver revisões).

---

### Evoluir o schema (modelos em `models/` mudaram)

Gere uma **nova** revisão e aplique:

```bash
flask --app 'app:create_app' db migrate -m "descrição curta da mudança"
flask --app 'app:create_app' db upgrade
```

---

### Outros comandos úteis

| Objetivo | Comando |
|----------|---------|
| Aplicar migrações pendentes | `flask --app 'app:create_app' db upgrade` |
| Revisão atual do banco | `flask --app 'app:create_app' db current` |
| Histórico de revisões | `flask --app 'app:create_app' db history` |
| Reverter a última migração (cuidado) | `flask --app 'app:create_app' db downgrade` |

Rotinas extras (por exemplo **refazer só o SQLite** ou **apagar banco e revisões e gerar `initial` de novo**, com variantes para Windows) estão em **[`docs/comandos-uteis.md`](docs/comandos-uteis.md)**.

---

## Git, `.gitignore` e banco versionado

No **`.gitignore` atual**:

- **`database/`** (`database/**`): o SQLite **não** entra no repositório por padrão. Cada pessoa cria o arquivo localmente com os fluxos **A**, **B** ou **C** acima.
- **`migrations/versions/`**: os `.py` de revisão **não** sobem no Git. Quem clona costuma estar no fluxo **A** (`db migrate` + `db upgrade`). Se a equipe passar a **versionar** `migrations/versions/`, remova essa linha do `.gitignore` e documente o fluxo **B** como padrão após o clone.

**Opcional:** remover a regra de **`database/`** se quiser versionar o arquivo SQLite (dados/fixture). Mesmo assim, após mudanças de modelo, **`db upgrade`** continua recomendado quando houver revisões novas.

## Como executar a API

### Modo desenvolvimento (recomendado para uso local)

```bash
python app.py
```

Por padrão o servidor sobe com **debug** ativado (veja `app.py`).

### Alternativa com o CLI do Flask

```bash
flask --app 'app:create_app' run --debug
```

A API fica disponível em **http://127.0.0.1:5000** (porta padrão do Flask), salvo configuração contrária. Documentação OpenAPI em **`/openapi`** (ou redirecionamento a partir de `/`).

Uma cópia destes comandos está em **[`docs/comandos-uteis.md`](docs/comandos-uteis.md#executar-a-api)**.

## Documentação e rotas principais

| Recurso | Descrição |
|--------|-----------|
| `GET /` | Redireciona para a documentação OpenAPI |
| Documentação interativa | Acesse **`/openapi`** após subir o servidor |
| `POST /rent` | Criar aluguel |
| `GET /rent` | Listar aluguéis |
| `GET /rent/<id>` | Buscar aluguel por identificador |

**CORS** está habilitado na aplicação para consumo a partir de outros origens em desenvolvimento.

## Estrutura relevante do projeto

- `docs/comandos-uteis.md` — comandos de terminal (migrações, banco, servidor)
- `app.py` — fábrica da aplicação (`create_app`) e definição das rotas
- `config.py` — URI do SQLite e demais configurações
- `extensions.py` — SQLAlchemy e Migrate
- `models/` — modelos ORM
- `schemas/` — esquemas de validação (Pydantic) e parâmetros de rota
- `services/` — lógica de negócio
- `migrations/` — Alembic (`env.py`, etc.); revisões em `migrations/versions/`
