# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes_zodb.mongo_connector import comentarios_collection
from datetime import datetime
from bson import ObjectId

class ComentarioCreateView(APIView):
    def post(self, request):
        data = request.data
        comentario = {
            "jogo_id": int(data["jogo_id"]),
            "cliente_id": request.user.id,
            "nota": float(data["nota"]),
            "comentario": data["comentario"],
            "data": datetime.now()
        }
        result = comentarios_collection.insert_one(comentario)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

    def get(self, request):
        comentarios = list(comentarios_collection.find())
        for c in comentarios:
            c["_id"] = str(c["_id"])
            c["data"] = c["data"].isoformat()
        return Response(comentarios, status=status.HTTP_200_OK)

    def put(self, request):
        comentario_id = request.data.get("id")
        if not comentario_id:
            return Response({"erro": "ID do comentário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filtro = {"_id": ObjectId(comentario_id), "cliente_id": request.user.id}
            atualizacao = {
                "$set": {

                    "nota": float(request.data.get("nota", 0)),
                    "comentario": request.data.get("comentario", ""),
                    "data": datetime.now()
                }
            }
            result = comentarios_collection.update_one(filtro, atualizacao)
            if result.matched_count == 0:
                return Response({"erro": "Comentário não encontrado ou não pertence ao usuário."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"mensagem": "Comentário atualizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comentario_id = request.data.get("id")
        if not comentario_id:
            return Response({"erro": "ID do comentário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filtro = {"_id": ObjectId(comentario_id), "cliente_id": request.user.id}
            result = comentarios_collection.delete_one(filtro)
            # if result.deleted_count == 0:
                # return Response({"erro": "Comentário não encontrado ou não pertence ao usuário."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"mensagem": "Comentário deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
