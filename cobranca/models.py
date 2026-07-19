from django.db import models

from associados.models import Associado
from financeiro.models import PlanoDeContas


class Cobranca(models.Model):
    STATUS_PENDENTE = "PENDENTE"
    STATUS_PAGA = "PAGA"
    STATUS_CANCELADA = "CANCELADA"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGA, "Paga"),
        (STATUS_CANCELADA, "Cancelada"),
    ]

    associado = models.ForeignKey(
        Associado,
        on_delete=models.PROTECT,
        related_name="cobrancas",
        null=True,
        blank=True,
    )

    plano_conta = models.ForeignKey(
        PlanoDeContas,
        on_delete=models.PROTECT,
        related_name="cobrancas",
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    descricao = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
    )

    data_vencimento = models.DateField()

    codigo_gateway = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )

    link_pagamento = models.URLField(
        null=True,
        blank=True,
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-data_criacao"]
        verbose_name = "Cobrança"
        verbose_name_plural = "Cobranças"

    def __str__(self):
        associado = (
            self.associado.razao_social
            if self.associado
            else "Sem associado"
        )

        return (
            f"Cobrança {self.pk} - "
            f"{associado} - "
            f"{self.status}"
        )