from db import consultar, executar


def listar():
    return consultar(
        "SELECT idMecanico AS id, nome, especialidade FROM mecanicos ORDER BY nome"
    )


def buscar(mecanico_id):
    return consultar(
        "SELECT idMecanico AS id, nome, especialidade FROM mecanicos WHERE idMecanico = %s",
        (mecanico_id,),
        um=True,
    )


def inserir(nome, especialidade):
    return executar(
        "INSERT INTO mecanicos (nome, especialidade) VALUES (%s, %s)",
        (nome, especialidade),
    )


def atualizar(mecanico_id, nome, especialidade):
    executar(
        "UPDATE mecanicos SET nome = %s, especialidade = %s WHERE idMecanico = %s",
        (nome, especialidade, mecanico_id),
    )


def excluir(mecanico_id):
    executar("DELETE FROM mecanicos WHERE idMecanico = %s", (mecanico_id,))
