from db import consultar, executar


def listar():
    return consultar(
        "SELECT idCliente AS id, nome, telefone, email FROM clientes ORDER BY nome"
    )


def buscar(cliente_id):
    return consultar(
        "SELECT idCliente AS id, nome, telefone, email FROM clientes WHERE idCliente = %s",
        (cliente_id,),
        um=True,
    )


def inserir(nome, telefone, email):
    return executar(
        "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
        (nome, telefone, email),
    )


def atualizar(cliente_id, nome, telefone, email):
    executar(
        "UPDATE clientes SET nome = %s, telefone = %s, email = %s WHERE idCliente = %s",
        (nome, telefone, email, cliente_id),
    )


def excluir(cliente_id):
    executar("DELETE FROM clientes WHERE idCliente = %s", (cliente_id,))
