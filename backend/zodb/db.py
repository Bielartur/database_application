from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction
from zodb_models.jogo import Jogo
from zodb_models.usuario import Usuario


class BaseDB():
    def __init__(self):
        self.storage = FileStorage.FileStorage('jogos.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()


class JogoDB(BaseDB):
    def __init__(self):        
        super().__init__()

        # Inicializa as "tabelas" se não existirem
        if not hasattr(self.root, 'jogos'):
            self.root.jogos = OOBTree()

    # Métodos para jogo
    def criar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()

    def buscar_jogo(self, id) -> Jogo:
        return self.root.jogos.get(id)
    
    def listar_jogos(self) -> list[Jogo]:
        return list(self.root.jogos.values())
    
    def atualizar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()
    
    def excluir_jogo(self, id: int) -> Jogo:
        jogo = self.buscar_jogo(id)
        if jogo:
            del self.root.jogos[jogo.id]
            transaction.commit()
            return jogo

    # Métodos para Usuário
    def criar_usuario(self, usuario: Usuario):
        self.root.usuario[usuario.id] = usuario
        transaction.commit()

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
        transaction.commit()

    def excluir_usuario(self, id: int) -> Usuario:
        usuario = self.buscar_usuario(id)
        if usuario:
            del self.root.usuarios[usuario.id]
            transaction.commit()
            return usuario

     
# class UsuarioDB(BaseDB):
#     def __init__(self):
#         super().__init__()

#         # Inicializa as "tabelas" se não existirem
#         if not hasattr(self.root, 'usuarios'):
#             self.root.usuarios = OOBTree()


    