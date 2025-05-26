from persistent import Persistent

class Jogo(Persistent):
  
  def __init__(self, id: int, titulo: str, descricao: str, ano: int, categoria: str, duracao: int, preco: float, url_imagem: str):
    self.id = id
    self.titulo = titulo
    self.descricao = descricao
    self.ano = ano
    self.categoria = categoria
    self.duracao = duracao
    self.preco = preco
    self.url_imagem = url_imagem
      
class Usuario(Persistent):
  def __init__(self, id: int, nome: str, email: str, senha: str):
    self.id = id
    self.nome = nome
    self.email = email
    self.senha = senha