# Oficina Mecânica · Revenda de Automóveis

Sistema web para controle de atendimentos de uma oficina mecânica integrada a uma revenda de automóveis. Feito com Python, Flask e MySQL, com consultas SQL escritas à mão (sem ORM).

A aplicação e o banco rodam em containers Docker. O banco é criado automaticamente a partir do `banco.sql` na primeira vez que o projeto sobe.

## Funcionalidades

| Tela | Rota | Descrição |
| --- | --- | --- |
| Início | `/` | Atalhos para todas as seções |
| Clientes | `/clientes` | Cadastro, edição e exclusão |
| Veículos | `/veiculos` | Cadastro, edição e exclusão |
| Mecânicos | `/mecanicos` | Cadastro, edição e exclusão |
| Serviços | `/servicos` | Cadastro, edição e exclusão |
| Nova ordem de serviço | `/ordens/nova` | Cliente, veículo, mecânico, serviço, data de abertura e observações |
| Ordens de serviço | `/ordens` | Consulta com `INNER JOIN` entre seis tabelas |
| Relatório gerencial | `/relatorios/mecanicos` | Mecânicos que mais realizaram serviços (`GROUP BY` + `COUNT`) |

Registros usados em alguma ordem de serviço não podem ser excluídos (integridade referencial), e a aplicação avisa quando isso acontece.

## Estrutura

O projeto segue o padrão MVC:

```text
.
├── app/
│   ├── app.py               # Cria o Flask e registra as rotas
│   ├── db.py                # Conexão com o MySQL
│   ├── models/              # Model: consultas SQL de cada tabela
│   │   ├── cliente.py
│   │   ├── veiculo.py
│   │   ├── mecanico.py
│   │   ├── servico.py
│   │   ├── ordem_servico.py # INNER JOIN da consulta de ordens
│   │   └── relatorio.py     # GROUP BY / COUNT do relatório
│   ├── controllers/         # Controller: rotas (blueprints) de cada seção
│   ├── services/            # Regras de negócio
│   ├── templates/           # View: páginas HTML (Jinja2)
│   └── static/              # CSS
├── banco.sql                # Criação do banco e das tabelas
├── requirements.txt         # Dependências Python
├── Dockerfile
├── docker-compose.yml       # Serviços: web (Flask) e db (MySQL 8.0)
├── .env.example
└── README.md
```

## Como executar

O projeto pode ser executado **com Docker** (mais simples: o MySQL vem junto e o banco é criado sozinho) ou **sem Docker** (usando Python e MySQL instalados no computador).

### 1. Configurar o `.env` (obrigatório nos dois modos)

Na pasta raiz do projeto, copie o arquivo de exemplo:

Linux:

```bash
cp .env.example .env
```

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Depois abra o `.env` e ajuste a senha:

| Variável | Valor inicial | Descrição |
| --- | --- | --- |
| `MYSQL_HOST` | `localhost` | Endereço do MySQL. No Docker é trocado automaticamente para `db` |
| `MYSQL_PORT` | `3306` | Porta do MySQL |
| `MYSQL_USER` | `root` | Usuário do MySQL |
| `MYSQL_PASSWORD` | `sua_senha` | Com Docker: senha que o MySQL do container vai usar. Sem Docker: senha do seu MySQL instalado |
| `MYSQL_DATABASE` | `oficina` | Banco criado pelo `banco.sql` |
| `SECRET_KEY` | `troque-esta-chave` | Chave do Flask para as mensagens de aviso |

### 2a. Executar com Docker

**Pré-requisito:** Docker instalado e em execução (no Windows, o Docker Desktop). Não é preciso instalar Python nem MySQL.

Na pasta raiz do projeto (o comando é o mesmo no Linux e no Windows):

```bash
docker compose up -d --build
```

Na primeira execução, o MySQL roda o `banco.sql` e cria o banco `oficina` com todas as tabelas. O Flask só inicia depois que o banco está pronto.

Para parar:

```bash
docker compose down
```

#### Acessar o banco do Docker

Pelo terminal:

```bash
docker compose exec db mysql -uroot -p oficina
```

Pelo MySQL Workbench ou outro cliente: host `127.0.0.1`, porta `3307`, usuário `root` e a senha do `.env`. A porta 3307 evita conflito com um MySQL que já esteja instalado no computador.

#### Recriar o banco do Docker

O `banco.sql` só é executado quando o volume do banco está vazio. Depois de alterar o script, apague o volume e suba de novo:

```bash
docker compose down -v
docker compose up -d --build
```

Atenção: `down -v` apaga todos os dados do banco.

### 2b. Executar sem Docker

**Pré-requisitos:** Python 3 e MySQL instalados, com o MySQL em execução na porta `3306`.

#### Linux

```bash
# 1. Criar o ambiente virtual e instalar as dependências (só na primeira vez)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Criar o banco (só na primeira vez; pede a senha do MySQL)
mysql -u root -p < banco.sql

# 3. Rodar a aplicação
.venv/bin/python app/app.py
```

#### Windows (PowerShell)

```powershell
# 1. Criar o ambiente virtual e instalar as dependências (só na primeira vez)
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 2. Criar o banco (só na primeira vez; pede a senha do MySQL)
cmd /c "mysql -u root -p < banco.sql"

# 3. Rodar a aplicação
.venv\Scripts\python app\app.py
```

Se o comando `mysql` não for reconhecido no Windows, crie o banco pelo **MySQL Workbench**: *File → Open SQL Script*, selecione o `banco.sql` e execute com o raio (⚡).

Para parar a aplicação, pressione `Ctrl+C` no terminal.

### 3. Acessar a aplicação

Nos dois modos, a aplicação fica disponível em:

```text
http://localhost:5000
```

A página inicial mostra se a conexão com o banco funcionou.

## Comandos úteis (Docker)

Verificar o status dos containers:

```bash
docker compose ps
```

Ver os logs da aplicação ou do banco:

```bash
docker compose logs -f web
docker compose logs -f db
```

## Solução de problemas

### `dependency failed to start: container ... db ... exited (1)`

O `banco.sql` tem algum erro. Veja qual com:

```bash
docker compose logs db | grep ERROR
```

Corrija o script e recrie o banco com `docker compose down -v`.

### `Access denied for user`

- **Com Docker:** a senha do `root` é definida só na criação do volume. Se `MYSQL_PASSWORD` mudou depois disso, recrie o banco com `docker compose down -v`.
- **Sem Docker:** confira se `MYSQL_USER` e `MYSQL_PASSWORD` no `.env` são os do seu MySQL instalado.

### `Unknown database 'oficina'` (sem Docker)

O banco ainda não foi criado. Rode o `banco.sql` conforme o passo 2 de "Executar sem Docker".

### `Can't connect to MySQL server` (sem Docker)

O MySQL não está em execução ou não está na porta do `.env`. No Linux, verifique com `systemctl status mysql`; no Windows, abra *Serviços* (`services.msc`) e confira se o serviço MySQL está *Em execução*.

### Porta 5000 ou 3307 ocupada

Altere a porta publicada no `docker-compose.yml`, por exemplo:

```yaml
ports:
  - "5001:5000"
```

Nesse caso, acesse `http://localhost:5001`.
