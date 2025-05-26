class ComentarioMongo:
    def __init__(self, jogo_id, cliente_id, nota, comentario, data):
        self.data = {
            "jogo_id": jogo_id,
            "cliente_id": cliente_id,
            "nota": nota,
            "comentario": comentario,
            "data": data
        }

class ImagemMongo:
    def __init__(self, jogo_id, url, descricao):
        self.data = {
            "jogo_id": jogo_id,
            "url": url,
            "descricao": descricao
        }
