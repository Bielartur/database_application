# clientes_zodb/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes_zodb.services.zodb_service import get_jogo_db
from clientes_zodb.models.zodb_models import Jogo
from clientes_zodb.utils.indentificar_id import identificar_novo_id
from etl.etl_runner import main as etl_main  # Adicionado import do ETL
import transaction


class JogoListCreate(APIView):
    def get(self, request, jogo_id=None):
        with get_jogo_db() as db:
            if jogo_id is not None:
                jogo = db.buscar_jogo_id(jogo_id)
                if not jogo:
                    return Response(
                        {'mensagem': f'Jogo com ID {jogo_id} não encontrado'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                data = {
                    "id": jogo.id,
                    "titulo": jogo.titulo,
                    "descricao": jogo.descricao,
                    "ano": jogo.ano,
                    "categoria": jogo.categoria,
                    "duracao": jogo.duracao,
                    "preco": jogo.preco
                }
                return Response(data, status=status.HTTP_200_OK)

            # Sem jogo_id: listar todos
            jogos = db.listar_jogos()
            data = [
                {
                    "id": jogo.id,
                    "titulo": jogo.titulo,
                    "descricao": jogo.descricao,
                    "ano": jogo.ano,
                    "categoria": jogo.categoria,
                    "duracao": jogo.duracao,
                    "preco": jogo.preco,
                    "url_imagem": jogo.url_imagem
                }
                for jogo in jogos
            ]
        if not data:
            return Response(
                {'mensagem': 'Nenhum jogo cadastrado ainda'},
                status=status.HTTP_200_OK
            )
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):     
        with get_jogo_db() as db:
            novo_id = identificar_novo_id('Jogo', db)
            dados = request.data
            jogo = Jogo(
                id=novo_id,
                titulo=dados['titulo'],
                descricao=dados['descricao'],
                ano=dados['ano'],
                categoria=dados['categoria'],
                duracao=dados['duracao'],
                preco=dados['preco'],
                url_imagem=dados['url_imagem']
            )
            db.criar_jogo(jogo)
            # Executa o ETL após criar o jogo
            # try:
            #     etl_main(db=db)
            # except Exception as e:
            #     print(f"Erro ao rodar ETL: {e}")
            transaction.commit()
        return Response({"mensagem": "Jogo criado", "id": novo_id,"dados": dados}, status=status.HTTP_201_CREATED)
    
    def put(self, request, jogo_id):
        dados = request.data
        with get_jogo_db() as db:
            jogo = db.buscar_jogo_id(jogo_id)

            if jogo is None:
                return Response({"erro": "Jogo não encontrado"}, status=404)

            # Atualiza os atributos
            jogo.titulo = dados.get('titulo', jogo.titulo)
            jogo.descricao = dados.get('descricao', jogo.descricao)
            jogo.ano = dados.get('ano', jogo.ano)
            jogo.categoria = dados.get('categoria', jogo.categoria)
            jogo.duracao = dados.get('duracao', jogo.duracao)
            jogo.preco = dados.get('preco', jogo.preco)
            jogo.url_imagem = dados.get('url_imagem', jogo.url_imagem)

            db.atualizar_jogo(jogo)  # você pode usar commit aqui também

            # Executa o ETL após atualizar o jogo
            # try:
            #     etl_main(db=db)
            # except Exception as e:
            #     print(f"Erro ao rodar ETL: {e}")
            transaction.commit()
        return Response({"mensagem": "Jogo atualizado"}, status=200)
    
    def delete(self, request, jogo_id):
        with get_jogo_db() as db:
            jogo = db.excluir_jogo(jogo_id)
            dados = {
                    "id": jogo.id,
                    "titulo": jogo.titulo,
                    "descricao": jogo.descricao,
                    "ano": jogo.ano,
                    "categoria": jogo.categoria,
                    "duracao": jogo.duracao,
                    "preco": jogo.preco
            }
            if jogo is None:
                return Response({"erro": "Jogo não encontrado"}, status=404)
            # Executa o ETL após deletar o jogo
            # try:
            #     etl_main(db=db)
            # except Exception as e:
            #     print(f"Erro ao rodar ETL: {e}")
            transaction.commit()
        return Response({"mensagem": "Jogo deletado", "dados": dados}, status=204)