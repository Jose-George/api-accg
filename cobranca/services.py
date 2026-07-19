from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Cobranca


class CobrancaService:
    @staticmethod
    def gerar_codigo_gateway():
        """
        Gera um identificador local para permitir o teste do webhook.

        Quando um gateway real for integrado, este código deverá ser
        substituído pelo identificador retornado pelo provedor.
        """
        while True:
            codigo = f"LOCAL-{uuid4().hex.upper()}"

            if not Cobranca.objects.filter(
                codigo_gateway=codigo
            ).exists():
                return codigo

    @staticmethod
    @transaction.atomic
    def processar_pagamento_gateway(codigo_gateway):
        """
        Localiza uma cobrança pelo código do gateway e altera o status
        para PAGA.

        O select_for_update evita que duas requisições simultâneas
        atualizem a mesma cobrança de forma concorrente.
        """
        codigo_gateway = str(codigo_gateway).strip()

        if not codigo_gateway:
            raise ValidationError(
                "O código do gateway não foi informado."
            )

        try:
            cobranca = (
                Cobranca.objects
                .select_for_update()
                .get(codigo_gateway=codigo_gateway)
            )
        except Cobranca.DoesNotExist as exc:
            raise ValidationError(
                "Cobrança não encontrada para o código informado."
            ) from exc

        if cobranca.status == Cobranca.STATUS_PAGA:
            return cobranca

        if cobranca.status == Cobranca.STATUS_CANCELADA:
            raise ValidationError(
                "Não é possível pagar uma cobrança cancelada."
            )

        cobranca.status = Cobranca.STATUS_PAGA
        cobranca.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )

        return cobranca