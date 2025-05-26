from clientes_zodb.services.zodb_service import JogoDB
from typing import Literal

def identificar_novo_id(tipo: Literal['Jogo', 'Usuário'], zodb: JogoDB) -> int:
    listas = {
        'Usuário': zodb.listar_usuarios(),
        'Jogo': zodb.listar_jogos(),
    }
    ultimo_id = listas[tipo][-1].id if listas[tipo] else 0
    return ultimo_id + 1