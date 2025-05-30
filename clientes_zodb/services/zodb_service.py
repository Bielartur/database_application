from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from contextlib import contextmanager

from clientes_zodb.models.zodb_models import Jogo
from clientes_zodb.models.zodb_models import Usuario


class BaseDB():
    def __init__(self):
        self.storage = FileStorage.FileStorage('zodb/jogos.fs')
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

        # Inicializa as "tabelas" se não existirem
        if not hasattr(self.root, 'jogos'):
            self.root.jogos = OOBTree()

        if not hasattr(self.root, 'usuarios'):
            self.root.usuarios = OOBTree()

    # Métodos para jogo
    def criar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo

    def buscar_jogo_id(self, id) -> Jogo:
        return self.root.jogos.get(id)
    
    def listar_jogos(self) -> list[Jogo]:
        return list(self.root.jogos.values())
    
    def atualizar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
    
    def excluir_jogo(self, id: int) -> Jogo:
        jogo = self.buscar_jogo_id(id)
        if jogo:
            del self.root.jogos[jogo.id]
            return jogo

    # Métodos para Usuário
    def criar_usuario(self, usuario: Usuario):
        self.root.usuario[usuario.id] = usuario

    def buscar_usuario_id(self, id) -> Usuario:
        return self.root.usuarios.get(id)
    
    def buscar_usuario_email(self, email) -> Usuario:
        for usuario in self.root.usuarios.values():  # Percorre todos os usuários
            if usuario.email == email:
                return usuario
    
    def listar_usuarios(self) -> list[Usuario]:
        return list(self.root.usuarios.values())
    
    def atualizar_usuario(self, usuario: Usuario):
        self.root.usuarios[usuario.id] = usuario

    def excluir_usuario(self, id: int) -> Usuario:
        usuario = self.buscar_usuario(id)
        if usuario:
            del self.root.usuarios[usuario.id]
            return usuario
        