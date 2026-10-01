from db import consultar


def mecanicos_mais_servicos():
    """Opção A: mecânicos que mais realizaram serviços (GROUP BY + COUNT)."""
    return consultar(
        """
        SELECT m.nome,
               m.especialidade,
               COUNT(osm.ordens_de_servico_idOS) AS total
        FROM mecanicos m
        LEFT JOIN ordens_de_servico_has_mecanicos osm
               ON osm.mecanicos_idMecanicos = m.idMecanico
        GROUP BY m.idMecanico, m.nome, m.especialidade
        ORDER BY total DESC, m.nome
        """
    )
