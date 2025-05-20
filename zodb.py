from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction
from zodb_models.jogo import Jogo

class JogoDB:
    def __init__(self):
        self.storage = FileStorage.FileStorage('jogos.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        
        # Inicializa as "tabelas" se não existirem
        if not hasattr(self.root, 'jogos'):
            self.root.jogos = OOBTree()

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

    # Métodos para jogo
    def criar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()

    def buscar_jogo(self, id):
        return self.root.jogos.get(id)
    
    def listar_jogos(self):
        return list(self.root.jogos.values())
    
    def atualizar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()
    
    def excluir_jogo(self, id: int):
        jogo = self.buscar_jogo(id)
        if jogo:
            del self.root.jogos[jogo.id]
            transaction.commit()
            return jogo