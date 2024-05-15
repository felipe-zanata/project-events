from django.db import models
from django.core.validators import RegexValidator

class Estado(models.Model):
    estado = models.CharField(max_length=255)
    sigla = models.CharField(max_length=2)
    cidades = models.TextField()  # Campo para armazenar as cidades em formato de lista
    

    def __str__(self):
        return f'{self.estado} - {self.sigla}'
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estado'
    
class Artista(models.Model):
    
    nome_artista = models.CharField(max_length=255, blank=False,null=False)
    nome_social = models.CharField(max_length=255, blank=True,null=True)
    telefone = models.CharField(max_length=17, blank=True)

    def __str__(self):
        return self.nome_social

    class Meta:
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

class DescricaoStatus(models.Model):
    descricao = models.CharField(max_length=255, blank=False,null=False)

    def __str__(self) -> str:
        return self.descricao
    
    class Meta:
        verbose_name = 'Descrição de Status'
        verbose_name_plural = 'Descrição de Status'
        
class AgendarEvento(models.Model):
    TIPO_DIARIA = [('S', 'Sim'), ('N', 'Não')]
    data_evento = models.DateField(blank=False,null=False)
    artista = models.ForeignKey(Artista, on_delete= models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete= models.PROTECT)
    uf = models.CharField(max_length=2, blank=True,null=True)
    cidade = models.CharField(max_length=100, blank=False,null=False)
    comissao = models.CharField(max_length=255, blank=True,null=True)
    producao = models.CharField(max_length=255, blank=True,null=True)
    valor_show = models.TextField()
    nome_vendedor =  models.CharField(max_length=100, blank=True,null=True)
    status = models.ForeignKey(DescricaoStatus, on_delete=models.PROTECT)
    data_enviado = models.DateField(blank=True,null=True)
    data_assinado = models.DateField(blank=True,null=True)
    diaria = models.CharField(max_length=1, choices=TIPO_DIARIA, blank=True, null=True)
    valor_diaria = models.CharField(max_length=255, blank=True,null=True)
    contato_nome_tel = models.CharField(max_length=255, blank=True,null=True)
    custos = models.CharField(max_length=255, blank=True,null=True)
    operacional = models.CharField(max_length=255, blank=True,null=True)
    obs = models.TextField(blank=True,null=True)
    anotacoes = models.TextField(blank=True,null=True)
    

    def __str__(self):
        return f'{self.estado}'

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

class Pagamentos(models.Model):
    evento = models.ForeignKey(AgendarEvento, on_delete=models.CASCADE)
    semana = models.CharField(max_length=255, blank=False,null=False)
    data_pagamento = models.DateField(blank=True,null=False)
    valor = models.CharField(max_length=255, blank=False,null=False)
    pagamento_status = models.CharField(max_length=255, blank=False,null=False)

    def __str__(self):
        return self.semana

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        
class OrigemDestinoKm(models.Model):
    origem = models.CharField(max_length=255, blank=True, null=True)
    destino = models.CharField(max_length=255, blank=True, null=True)
    km = models.CharField(max_length=255, blank=True, null=True)
    horas = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name     = 'Origem Destino'
