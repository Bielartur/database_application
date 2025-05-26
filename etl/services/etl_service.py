# etl/services/etl_service.py

from datetime import datetime, timedelta
import random
import logging
from clientes_zodb.services.zodb_service import JogoDB
from etl.models import DimJogo, DimTempo, FatoVenda

logger = logging.getLogger(__name__)

def insert_dim_jogo(jogo):
    obj, created = DimJogo.objects.get_or_create(
        titulo=jogo.titulo,
        ano=jogo.ano,
        defaults={
            "descricao": jogo.descricao,
            "categoria": jogo.categoria,
            "duracao": jogo.duracao
        }
    )
    return obj

def insert_dim_tempo(data):
    obj, _ = DimTempo.objects.get_or_create(
        data_venda=data,
        defaults={"ano": data.year, "mes": data.month, "dia": data.day}
    )
    return obj

def insert_fato_venda(jogo, tempo, preco, quantidade):
    return FatoVenda.objects.create(
        jogo=jogo,
        tempo=tempo,
        preco=preco,
        quantidade=quantidade
    )

def simular_vendas_para_jogo(jogo):
    for dias_atras in range(30):
        data = datetime.now().date() - timedelta(days=dias_atras)
        tempo = insert_dim_tempo(data)
        quantidade = random.randint(0, 5)
        if quantidade > 0:
            insert_fato_venda(jogo, tempo, jogo.preco, quantidade)
            logger.info(f"Venda simulada: {quantidade}x {jogo.titulo} em {data}")

def etl_zodb_to_dw():
    zodb = JogoDB()
    jogos = zodb.listar_jogos()
    logger.info(f"Jogos encontrados: {len(jogos)}")

    ids_zodb = set()
    for jogo in jogos:
        jogo_dw = insert_dim_jogo(jogo)
        ids_zodb.add(jogo_dw.jogo_id)
        simular_vendas_para_jogo(jogo_dw)

    # Remover jogos que não existem mais no ZODB
    DimJogo.objects.exclude(jogo_id__in=ids_zodb).delete()
    zodb.fechar()
    logger.info("ETL finalizado com sucesso.")
