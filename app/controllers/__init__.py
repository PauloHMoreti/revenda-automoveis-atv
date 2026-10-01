import re

from mysql.connector import Error as MySQLError

MENSAGENS_ERRO = {
    1062: "Já existe um registro com esse valor (e-mail ou placa duplicados).",
    1451: "Não é possível excluir: o registro está vinculado a uma ordem de serviço.",
    1452: "Registro relacionado não encontrado.",
    1406: "Algum campo ultrapassou o tamanho máximo permitido.",
    1264: "Algum valor numérico está fora do intervalo permitido.",
}


def mensagem_erro(erro: MySQLError):
    return MENSAGENS_ERRO.get(erro.errno, f"Erro no banco de dados: {erro.msg}")


def somente_digitos(texto):
    return re.sub(r"\D", "", texto or "")
