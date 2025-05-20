import persistent

class Jogo(persistent.Persistent):
  

  def __init__(self, id, titulo, descricao, ano, categoria, duracao, preco):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.ano = ano
        self.categoria = categoria
        self.duracao = duracao
        self.preco = preco