from db import consultar, executar


def listar():
    return consultar(
        "SELECT idVeiculo AS id, modelo, marca, ano, placa FROM veiculo ORDER BY marca, modelo"
    )


def buscar(veiculo_id):
    return consultar(
        "SELECT idVeiculo AS id, modelo, marca, ano, placa FROM veiculo WHERE idVeiculo = %s",
        (veiculo_id,),
        um=True,
    )


def inserir(modelo, marca, ano, placa):
    return executar(
        "INSERT INTO veiculo (modelo, marca, ano, placa) VALUES (%s, %s, %s, %s)",
        (modelo, marca, ano, placa),
    )


def atualizar(veiculo_id, modelo, marca, ano, placa):
    executar(
        "UPDATE veiculo SET modelo = %s, marca = %s, ano = %s, placa = %s WHERE idVeiculo = %s",
        (modelo, marca, ano, placa, veiculo_id),
    )


def excluir(veiculo_id):
    executar("DELETE FROM veiculo WHERE idVeiculo = %s", (veiculo_id,))
