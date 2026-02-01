from django.db import models
from financeiro.models import PlanoDeContas

# Create your models here.
class Cobranca(models.Model):

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga'),
        ('CANCELADA', 'Cancelada'),
    ]

    plano_conta = models.ForeignKey(
        PlanoDeContas,
        on_delete=models.PROTECT,
        related_name='cobrancas'
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descricao = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )

    data_vencimento = models.DateField()

    codigo_gateway = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    link_pagamento = models.URLField(
        null=True,
        blank=True
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Cobrança {self.id} - {self.status}"
