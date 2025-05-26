import sys
import os
import random
import logging
from datetime import datetime, timedelta

from clientes_zodb.services.zodb_service import JogoDB
from etl.models import DimJogo, DimTempo, FatoVenda

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def insert_dim_jogo(jogo):
    duracao = int(jogo.duracao.split(' ')[0])
    obj, created = DimJogo.objects.get_or_create(
        titulo=jogo.titulo,
        ano=jogo.ano,
        defaults={
            "descricao": jogo.descricao,
            "categoria": jogo.categoria,
            "duracao": duracao,
        }
    )
    return obj

def insert_dim_tempo(data_venda):
    obj, _ = DimTempo.objects.get_or_create(
        data_venda=data_venda,
        defaults={
            "ano": data_venda.year,
            "mes": data_venda.month,
            "dia": data_venda.day,
        }
    )
    return obj

def insert_fato_venda(jogo, tempo, preco, quantidade):
    FatoVenda.objects.create(
        jogo=jogo,
        tempo=tempo,
        preco=preco,
        quantidade=quantidade
    )

def simular_vendas_ultimos_30_dias(jogo_dw, preco):
    for dias_atras in range(30):
        data = datetime.now().date() - timedelta(days=dias_atras)
        tempo_dw = insert_dim_tempo(data)
        quantidade = random.randint(0, 5)
        if quantidade > 0:
            insert_fato_venda(jogo_dw, tempo_dw, preco, quantidade)
            logging.info(f"Venda simulada {quantidade}x '{jogo_dw.titulo}' em {data}")

def remover_jogos_antigos(jogos_zodb):
    ids_zodb = set(j.id for j in jogos_zodb)
    ids_dw = set(DimJogo.objects.values_list('jogo_id', flat=True))

    ids_para_remover = ids_dw - ids_zodb
    if ids_para_remover:
        FatoVenda.objects.filter(jogo_id__in=ids_para_remover).delete()
        DimJogo.objects.filter(id__in=ids_para_remover).delete()
        logging.info(f"Removidos jogos do DW: {ids_para_remover}")

def main(db: JogoDB):
    logging.info("Início do ETL de vendas")

    jogos = db.listar_jogos()
    logging.info(f"Jogos encontrados: {len(jogos)}")

    remover_jogos_antigos(jogos)

    for jogo in jogos:
        try:
            jogo_dw = insert_dim_jogo(jogo)
            simular_vendas_ultimos_30_dias(jogo_dw, jogo.preco)
        except Exception as e:
            logging.error(f"Erro com jogo {jogo.titulo}: {e}")

    logging.info("ETL finalizado com sucesso.")
