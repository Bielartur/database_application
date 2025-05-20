import ZODB, ZODB.FileStorage
import transaction
from zodb_models.jogo import Jogo
from mongo.connect import get_mongo_db
from mongo.comentario import novo_comentario

# === Setup ZODB ===
storage = ZODB.FileStorage.FileStorage('jogos.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

if 'jogos' not in root:
    root['jogos'] = {}

# === Setup MongoDB ===
db_mongo = get_mongo_db()
comentarios = db_mongo["comentarios"]

# === Funções ===
def criar_jogo():
    id = int(input("ID: "))
    if id in root['jogos']:
        print("⚠ Jogo com esse ID já existe.")
        return
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    ano = int(input("Ano: "))
    categoria = input("Categoria: ")
    duracao = int(input("Duração (min): "))
    preco = float(input("Preço: "))

    jogo = Jogo(id, titulo, descricao, ano, categoria, duracao, preco)
    root['jogos'][id] = jogo
    transaction.commit()
    print("✅ Jogo criado com sucesso.")

    add_comentario = input("Deseja adicionar comentário? (s/n) ").lower()
    if add_comentario == 's':
        criar_comentario(id)

def criar_comentario(jogo_id=None):
    if jogo_id is None:
        jogo_id = int(input("ID do jogo: "))
    cliente_id = input("ID do cliente: ")
    comentario_texto = input("Comentário: ")
    avaliacao = float(input("Avaliação (0-5): "))

    comentario = novo_comentario(jogo_id, cliente_id, comentario_texto, avaliacao)
    comentarios.insert_one(comentario)
    print("✅ Comentário adicionado.")

def listar_jogos():
    for id, jogo in root['jogos'].items():
        print(f"\n🎮 {jogo.id} - {jogo.titulo}")
        print(f"Descrição: {jogo.descricao}")
        print(f"Ano: {jogo.ano}, Categoria: {jogo.categoria}")
        print(f"Duração: {jogo.duracao}min, Preço: R${jogo.preco:.2f}")

def buscar_jogo():
    id = int(input("Digite o ID do jogo: "))
    if id in root['jogos']:
        jogo = root['jogos'][id]
        print(f"\n🎮 {jogo.id} - {jogo.titulo}")
        print(f"Descrição: {jogo.descricao}")
        print(f"Ano: {jogo.ano}, Categoria: {jogo.categoria}")
        print(f"Duração: {jogo.duracao}min, Preço: R${jogo.preco:.2f}")
        print("🗨 Comentários:")
        for c in comentarios.find({"jogo_id": str(id)}):
            print(f" - {c['cliente_id']}: {c['comentario']} ({c['avaliacao']}⭐)")
    else:
        print("❌ Jogo não encontrado.")

def atualizar_preco():
    id = int(input("ID do jogo: "))
    if id in root['jogos']:
        novo_preco = float(input("Novo preço: "))
        root['jogos'][id].preco = novo_preco
        transaction.commit()
        print("✅ Preço atualizado com sucesso.")
    else:
        print("❌ Jogo não encontrado.")

def remover_jogo():
    id = int(input("ID do jogo: "))
    if id in root['jogos']:
        del root['jogos'][id]
        transaction.commit()
        print("🗑 Jogo removido com sucesso.")
    else:
        print("❌ Jogo não encontrado.")

# === Menu Principal ===
def menu():
    while True:
        print("\n=== MENU ===")
        print("1 - Criar jogo")
        print("2 - Listar jogos")
        print("3 - Buscar jogo por ID")
        print("4 - Adicionar comentário")
        print("5 - Atualizar preço do jogo")
        print("6 - Remover jogo")
        print("0 - Sair")

        opcao = input("Escolha: ")
        if opcao == '1':
            criar_jogo()
        elif opcao == '2':
            listar_jogos()
        elif opcao == '3':
            buscar_jogo()
        elif opcao == '4':
            criar_comentario()
        elif opcao == '5':
            atualizar_preco()
        elif opcao == '6':
            remover_jogo()
        elif opcao == '0':
            break
        else:
            print("❌ Opção inválida.")

menu()

# === Fechamento ===
connection.close()
db.close()
