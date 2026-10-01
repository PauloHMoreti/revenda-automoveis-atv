from db import consultar, get_connection


def listar():
    """Consulta das ordens de serviço com INNER JOIN entre seis tabelas."""
    return consultar(
        """
        SELECT os.idOS                          AS id,
               c.nome                           AS cliente,
               CONCAT(v.marca, ' ', v.modelo)   AS veiculo,
               v.placa                          AS placa,
               m.nome                           AS mecanico,
               s.descricao                      AS servico,
               os.dataAbertura                  AS data_abertura,
               os.obs                           AS observacoes
        FROM ordens_de_servico os
        INNER JOIN clientes c
                ON c.idCliente = os.clientes_idClientes
        INNER JOIN veiculo v
                ON v.idVeiculo = os.veiculo_idVeiculo
        INNER JOIN servicos s
                ON s.idServico = os.servicos_idServico
        INNER JOIN ordens_de_servico_has_mecanicos osm
                ON osm.ordens_de_servico_idOS = os.idOS
               AND osm.ordens_de_servico_clientes_idClientes = os.clientes_idClientes
        INNER JOIN mecanicos m
                ON m.idMecanico = osm.mecanicos_idMecanicos
        ORDER BY os.dataAbertura DESC, os.idOS DESC
        """
    )


def inserir(cliente_id, veiculo_id, mecanico_id, servico_id, data_abertura, observacoes):
    """Grava a ordem e o mecânico responsável na mesma transação."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ordens_de_servico
                (dataAbertura, obs, clientes_idClientes, veiculo_idVeiculo, servicos_idServico)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data_abertura, observacoes, cliente_id, veiculo_id, servico_id),
        )
        ordem_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO ordens_de_servico_has_mecanicos
                (ordens_de_servico_idOS, ordens_de_servico_clientes_idClientes, mecanicos_idMecanicos)
            VALUES (%s, %s, %s)
            """,
            (ordem_id, cliente_id, mecanico_id),
        )
        conn.commit()
        return ordem_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
