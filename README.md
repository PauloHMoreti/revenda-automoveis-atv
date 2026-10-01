# Revenda de Automóveis

Aplicação web em Flask com banco MySQL, executados em containers Docker. O banco é criado automaticamente a partir do `banco.sql` na primeira vez que o projeto sobe.

## Estrutura

```text
.
├── app/
│   ├── app.py
│   ├── static/
│   └── templates/
├── banco.sql            # Criação do banco e das tabelas
├── requirements.txt
├── Dockerfile
├── docker-compose.yml   # Serviços: web (Flask) e db (MySQL 8.0)
├── .env.example
└── README.md
```

## Pré-requisitos

- Docker (Docker Desktop no Windows/macOS) instalado e em execução.

Não é preciso instalar o MySQL: ele roda no container `db`.

## Configuração

Copie o arquivo de exemplo e defina a senha:

```bash
cp .env.example .env
```

| Variável | Valor inicial | Descrição |
| --- | --- | --- |
| `MYSQL_HOST` | `localhost` | Usado só fora do Docker; no Compose é sempre `db` |
| `MYSQL_USER` | `root` | Usuário do MySQL |
| `MYSQL_PASSWORD` | `sua_senha` | Senha do `root` do container MySQL |
| `MYSQL_DATABASE` | `oficina` | Banco criado pelo `banco.sql` |

## Executar com Docker Compose

Na pasta raiz do projeto:

```bash
docker compose up -d --build
```

Na primeira execução, o MySQL roda o `banco.sql` e cria o banco `oficina` com todas as tabelas. O Flask só inicia depois que o banco está pronto.

A aplicação ficará disponível em:

```text
http://localhost:5000
```

A rota inicial testa a conexão com o banco e exibe o resultado na página.

### Acessar o banco

Pelo terminal:

```bash
docker compose exec db mysql -uroot -p oficina
```

Pelo MySQL Workbench ou outro cliente: host `127.0.0.1`, porta `3307`, usuário `root` e a senha do `.env`. A porta 3307 evita conflito com um MySQL que já esteja instalado no computador.

### Recriar o banco

O `banco.sql` só é executado quando o volume do banco está vazio. Depois de alterar o script, apague o volume e suba de novo:

```bash
docker compose down -v
docker compose up -d --build
```

Atenção: `down -v` apaga todos os dados do banco.

## Comandos úteis

Verificar o status dos containers:

```bash
docker compose ps
```

Ver os logs da aplicação ou do banco:

```bash
docker compose logs -f web
docker compose logs -f db
```

Parar os containers (os dados do banco são mantidos):

```bash
docker compose down
```

## Solução de problemas

### `dependency failed to start: container ... db ... exited (1)`

O `banco.sql` tem algum erro. Veja qual com:

```bash
docker compose logs db | grep ERROR
```

Corrija o script e recrie o banco com `docker compose down -v`.

### `Access denied for user`

A senha do `root` é definida só na criação do volume. Se `MYSQL_PASSWORD` mudou depois disso, recrie o banco com `docker compose down -v`.

### Porta 5000 ou 3307 ocupada

Altere a porta publicada no `docker-compose.yml`, por exemplo:

```yaml
ports:
  - "5001:5000"
```

Nesse caso, acesse `http://localhost:5001`.
