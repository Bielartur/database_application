from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

comentarios_collection = db["comentarios"]
imagens_collection = db["imagens"]
