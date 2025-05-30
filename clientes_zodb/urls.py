from django.urls import path
from .views.jogo_view import JogoListCreate
from .views.usuario_view import UsuarioListCreate
from .views.comentario_view import ComentarioCreateView

urlpatterns = [
    path('jogos/', JogoListCreate.as_view(), name='jogos'),
    path('jogos/<int:jogo_id>', JogoListCreate.as_view(), name='jogo-detalhe'),
    path('clientes/', UsuarioListCreate.as_view(), name='clientes'),
    path('comentarios/', ComentarioCreateView.as_view(), name='comentarios')
]
