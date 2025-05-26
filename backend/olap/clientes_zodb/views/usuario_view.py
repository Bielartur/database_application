# clientes_zodb/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes_zodb.services.zodb_service import JogoDB
from clientes_zodb.models.zodb_models import Usuario
from clientes_zodb.utils.indentificar_id import identificar_novo_id
import bcrypt


class UsuarioListCreate(APIView):
    def get(self, request):
        db = JogoDB()
        usuarios = db.listar_usuarios()
        data = [
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email
            }
            for u in usuarios
        ]
        db.fechar()
        return Response(data)

    def post(self, request):
        db = JogoDB()
        dados = request.data
        email = dados.get("email")

        # Verifica se e-mail já está cadastrado
        if db.buscar_usuario_email(email):
            db.fechar()
            return Response({"erro": "Email já existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Gera novo ID automático
        novo_id = identificar_novo_id('Usuário', db)

        # Hasheia a senha
        senha_hash = bcrypt.hashpw(dados['senha'].encode(), bcrypt.gensalt())

        usuario = Usuario(
            id=novo_id,
            nome=dados['nome'],
            email=email,
            senha=senha_hash.decode()  # Armazena como string
        )

        db.criar_usuario(usuario)
        db.fechar()
        return Response({"mensagem": "Usuário criado", "id": novo_id}, status=status.HTTP_201_CREATED)
