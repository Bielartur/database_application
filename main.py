from zodb import JogoDB
from zodb_models.jogo import Jogo
from mongo.connect import get_mongo_db
from mongo.comentario import novo_comentario

from time import sleep

# === Setup ZODB ===
zodb = JogoDB()
# === Setup MongoDB ===
db_mongo = get_mongo_db()
comentarios = db_mongo["comentarios"]

# === Cores ===
def amarelo(texto: str) -> str:
    return f'\033[33m{texto}\033[0m'

def verde(texto: str) -> str:
    return f'\033[32m{texto}\033[0m'

def ciano(texto: str) -> str:
    return f'\033[36m{texto}\033[0m'

def azul(texto: str) -> str:
    return f'\033[34m{texto}\033[0m'

def vermelho(texto:str) -> str:
    return f'\033[31m{texto}\033[0m'

def roxo(texto: str) -> str:
    return f'\033[35m{texto}\033[0m'

def laranja(texto: str) -> str:
    return f'\033[33m{texto}\033[0m'

# === Funções ===
def criar_jogo():
    id = int(input("ID: "))
    if zodb.buscar_jogo(id):
        print("⚠ Jogo com esse ID já existe.")
        return
    titulo = input(f"{ciano('Título')}: ")
    descricao = input(f"{roxo('Descrição')}: ")
    ano = int(input(f"{azul('Ano')}: "))
    categoria = input(f"{laranja('Categoria')}: ")
    duracao = int(input(f"{verde('Duração')} (min): "))
    preco = float(input(f"{vermelho('Preço')}: "))

    jogo = Jogo(id, titulo, descricao, ano, categoria, duracao, preco)
    zodb.criar_jogo(jogo)
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
    jogos = zodb.listar_jogos()
    for jogo in jogos:
        print(f"\n🎮 {jogo.id} - {ciano(jogo.titulo)}")
        print(f"    {roxo('Descrição')}: {jogo.descricao}")
        print(f"    {azul('Ano')}: {jogo.ano}")
        print(f"    {laranja('Categoria')}: {jogo.categoria}")
        print(f"    {verde('Duração')}: {jogo.duracao}min")
        print(f"    {vermelho('Preço')}: R${jogo.preco:.2f}")
    sleep(1)

def buscar_jogo():
    id = int(input("Digite o ID do jogo: "))
    jogo = zodb.buscar_jogo(id)
    if jogo:
        print(f"\n🎮 {jogo.id} - {ciano(jogo.titulo)}")
        print(f"    {roxo('Descrição')}: {jogo.descricao}")
        print(f"    {azul('Ano')}: {jogo.ano}")
        print(f"    {laranja('Categoria')}: {jogo.categoria}")
        print(f"    {verde('Duração')}: {jogo.duracao}min")
        print(f"    {vermelho('Preço')}: R${jogo.preco:.2f}")
        print("🗨 Comentários:")
        for c in comentarios.find({"jogo_id": str(id)}):
            print(f" - {c['cliente_id']}: {c['comentario']} ({c['avaliacao']}⭐)")
    else:
        print("❌ Jogo não encontrado.")

def atualizar_info():
    id = int(input("ID do jogo: "))
    jogo = zodb.buscar_jogo(id)
    if jogo:
        valores = infos_para_atualizar(jogo)
        jogo_atualizado = Jogo(id, **valores)
        zodb.atualizar_jogo(jogo_atualizado)
        print("✅ Preço atualizado com sucesso.")
    else:
        print("❌ Jogo não encontrado.")

def infos_para_atualizar(jogo: Jogo):
    opcoes = {
        '1': (ciano('Título'), 'titulo'),
        '2': (roxo('Descrição'), 'descricao'),
        '3': (azul('Ano'), 'ano'),
        '4': (laranja('Categoria'), 'categoria'),
        '5': (verde('Duração'), 'duracao'),
        '6': (vermelho('Preço'), 'preco'),
    }

    while True:
        print('\nO que você deseja atualizar?')
        for k, (nome, _) in opcoes.items():
            print(f'{k} - {nome}')
        print('0 - Sair')

        entrada = input("Escolha as opções separadas por vírgula (ex: 1,2,5): ").split(',')
        entrada = [op.strip() for op in entrada]

        if '0' in entrada:
            print("Saindo da atualização.")
            break

        valores = {}

        for codigo, (nome, atributo) in opcoes.items():
            if codigo in entrada:
                novo_valor = input(f'Novo(a) {nome}: ')
                if atributo == 'preco':
                    novo_valor = float(novo_valor)

                if atributo == 'ano':
                    novo_valor = int(novo_valor)

                if atributo == 'duracao':
                    novo_valor = int(novo_valor)
                valores[atributo] = novo_valor
            else:
                valores[atributo] = getattr(jogo, atributo)

        # Aqui você pode retornar os novos valores ou atualizar diretamente o objeto
        return valores


def remover_jogo():
    id = int(input("ID do jogo: "))
    jogo = zodb.excluir_jogo(id)
    if jogo:
        print("🗑 Jogo removido com sucesso.")
    else:
        print("❌ Jogo não encontrado.")

# === Menu Principal ===
def menu():
    try:
        while True:
            print("\n=== MENU ===")
            print("1 - Criar jogo")
            print("2 - Listar jogos")
            print("3 - Buscar jogo por ID")
            print("4 - Adicionar comentário")
            print("5 - Atualizar informações do jogo")
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
                atualizar_info()
            elif opcao == '6':
                remover_jogo()
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida.")
    finally:
        zodb.fechar()

menu()
