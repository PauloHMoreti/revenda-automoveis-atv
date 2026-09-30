# Revenda de Automóveis

Aplicação web em Flask executada em Docker e conectada a um servidor MySQL instalado no computador host.

## Estrutura

```text
.
├── app/
│   ├── app.py
│   ├── static/
│   │   ├── style.css
│   │   └── ...
│   └── templates/
│       └── index.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

- Docker Desktop instalado e em execução.
- MySQL instalado no host e escutando na porta `3306`.
- Um banco de dados criado no MySQL.

O container acessa o MySQL do Windows usando `host.docker.internal`. Não é criado um segundo container MySQL.

## Configuração do banco

Crie o banco, caso ainda não exista:

```sql
CREATE DATABASE meubanco;
```

As configurações usadas pela aplicação são:

| Variável | Valor inicial | Descrição |
| --- | --- | --- |
| `MYSQL_HOST` | `host.docker.internal` | Endereço do MySQL no host |
| `MYSQL_USER` | `root` | Usuário do MySQL |
| `MYSQL_PASSWORD` | `sua_senha` | Senha do usuário |
| `MYSQL_DATABASE` | `meubanco` | Banco utilizado pela aplicação |

## Executar com Docker Compose

Edite o arquivo `.env` na raiz do projeto e informe as credenciais da sua instalação do MySQL:

```dotenv
MYSQL_USER=root
MYSQL_PASSWORD=SUA_SENHA_REAL
MYSQL_DATABASE=meubanco
```

Depois, na pasta raiz do projeto, execute:

```powershell
docker compose up -d --build
```

A aplicação ficará disponível em:

```text
http://localhost:5000
```

A rota inicial testa a conexão com o banco executando uma consulta simples e exibe uma mensagem na página.

## Comandos úteis

Verificar o status do container:

```powershell
docker compose ps
```

Ver os logs da aplicação:

```powershell
docker compose logs -f web
```

Reconstruir a imagem sem usar cache:

```powershell
docker compose build --no-cache
docker compose up -d
```

Parar e remover o container:

```powershell
docker compose down
```

## Solução de problemas

### `Access denied for user`

Confira `MYSQL_USER`, `MYSQL_PASSWORD` e `MYSQL_DATABASE` no arquivo `.env`. Depois recrie o container para aplicar as variáveis:

```powershell
docker compose down
docker compose up -d --build
```

### Erro de conexão com o MySQL

Confirme se o serviço MySQL está em execução e se a porta está aberta:

```powershell
Test-NetConnection localhost -Port 3306
```

O resultado esperado para `TcpTestSucceeded` é `True`.

### Porta 5000 ocupada

Altere a porta publicada no `docker-compose.yml`, por exemplo:

```yaml
ports:
  - "5001:5000"
```

Nesse caso, acesse `http://localhost:5001`.
