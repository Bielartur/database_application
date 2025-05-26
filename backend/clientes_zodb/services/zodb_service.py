from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction
from contextlib import contextmanager

from clientes_zodb.models.zodb_models import Jogo, Usuario


class BaseDB:
    def __init__(self):
        self.storage = FileStorage.FileStorage('zodb/jogos.fs')  # Considere mover para fora do OneDrive
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()


@contextmanager
def get_jogo_db():
    db = JogoDB()
    try:
        yield db
    finally:
        db.fechar()


class JogoDB(BaseDB):
    def __init__(self):
        super().__init__()

        if not hasattr(self.root, 'jogos'):
            self.root.jogos = OOBTree()

        if not hasattr(self.root, 'usuarios'):
            self.root.usuarios = OOBTree()

    # Métodos para Jogo
    def criar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()

    def buscar_jogo_id(self, id) -> Jogo:
        return self.root.jogos.get(id)

    def listar_jogos(self) -> list[Jogo]:
        return list(self.root.jogos.values())

    def atualizar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
