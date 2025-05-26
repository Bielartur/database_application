from django.db import models

class DimJogo(models.Model):
    jogo_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    ano = models.IntegerField()
    categoria = models.CharField(max_length=100)
    duracao = models.IntegerField()

    class Meta:
        db_table = 'dw.dim_jogo'

class DimTempo(models.Model):
    tempo_id = models.AutoField(primary_key=True)
    data_venda = models.DateField(unique=True)
    ano = models.IntegerField()
    mes = models.IntegerField()
    dia = models.IntegerField()

    class Meta:
        db_table = 'dw.dim_tempo'

class FatoVenda(models.Model):
    id = models.AutoField(primary_key=True)
    jogo = models.ForeignKey(DimJogo, on_delete=models.CASCADE)
    tempo = models.ForeignKey(DimTempo, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()

    class Meta: 
        db_table = 'dw.fato_venda'

