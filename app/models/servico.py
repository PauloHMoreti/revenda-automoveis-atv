from db import consultar, executar


def listar():
    return consultar(
        "SELECT idServico AS id, descricao, valor FROM servicos ORDER BY descricao"
    )


def buscar(servico_id):
    return consultar(
        "SELECT idServico AS id, descricao, valor FROM servicos WHERE idServico = %s",
        (servico_id,),
        um=True,
    )


def inserir(descricao, valor):
    return executar(
        "INSERT INTO servicos (descricao, valor) VALUES (%s, %s)",
        (descricao, valor),
    )


def atualizar(servico_id, descricao, valor):
    executar(
        "UPDATE servicos SET descricao = %s, valor = %s WHERE idServico = %s",
        (descricao, valor, servico_id),
    )


def excluir(servico_id):
    executar("DELETE FROM servicos WHERE idServico = %s", (servico_id,))
