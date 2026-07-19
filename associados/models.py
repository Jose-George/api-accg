from datetime import timedelta

from django.db import models
from django.utils import timezone


class Associado(models.Model):
    STATUS_ATIVO = "ATIVO"
    STATUS_INATIVO = "INATIVO"
    STATUS_SUSPENSO = "SUSPENSO"

    STATUS_CHOICES = [
        (STATUS_ATIVO, "Ativo"),
        (STATUS_INATIVO, "Inativo"),
        (STATUS_SUSPENSO, "Suspenso"),
    ]

    razao_social = models.CharField(
        max_length=255,
    )

    nome_fantasia = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    cnpj = models.CharField(
        max_length=14,
        unique=True,
    )

    email = models.EmailField()

    telefone = models.CharField(
        max_length=20,
    )

    endereco = models.TextField()

    contrato = models.FileField(
        upload_to="contratos/",
        null=True,
        blank=True,
    )

    ficha_cadastral = models.FileField(
        upload_to="fichas/",
        null=True,
        blank=True,
    )

    data_vencimento = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_ATIVO,
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
    )

    data_ultimo_aviso = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["razao_social"]
        verbose_name = "Associado"
        verbose_name_plural = "Associados"

    def save(self, *args, **kwargs):
        # Define um ano somente quando nenhuma data foi informada.
        # Dessa forma, testes e cadastros administrativos podem
        # informar outra data de vencimento.
        if not self.data_vencimento:
            self.data_vencimento = (
                timezone.localdate()
                + timedelta(days=365)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.razao_social