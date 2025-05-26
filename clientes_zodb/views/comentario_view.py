# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes_zodb.mongo_connector import comentarios_collection
from datetime import datetime

class ComentarioCreateView(APIView):
    def post(self, request):
        data = request.data
        comentario = {
            "jogo_id": data["jogo_id"],
            "cliente_id": data["cliente_id"],
            "nota": float(data["nota"]),
            "comentario": data["comentario"],
            "data": datetime.now()
        }
        result = comentarios_collection.insert_one(comentario)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
