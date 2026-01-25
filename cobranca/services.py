from django.core.exceptions import ValidationError
from .models import Cobranca

class CobrancaService:
    @staticmethod
    def processar_pagamento_gateway(codigo_gateway):
        """
        Localiza uma cobrança pelo código do gateway e atualiza seu status para PAGA.
        Lança ValidationError caso a cobrança não exista ou já esteja paga/cancelada.
        """
        try:
            cobranca = Cobranca.objects.get(codigo_gateway=codigo_gateway)
        except Cobranca.DoesNotExist:
            raise ValidationError("Cobrança não encontrada para o código informado.")

        if cobranca.status == 'PAGA':
            # Idempotência: se já está paga, apenas retorna sucesso
            return cobranca
            
        if cobranca.status == 'CANCELADA':
            raise ValidationError("Não é possível pagar uma cobrança CANCELADA.")

        cobranca.status = 'PAGA'
        cobranca.save()
        return cobranca
