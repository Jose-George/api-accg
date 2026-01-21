from rest_framework import serializers
from .models import Cobranca

class CobrancaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cobranca
        fields = [
            'id',
            'plano_conta',
            'valor',
            'descricao',
            'status',
            'data_vencimento',
            'codigo_gateway',
            'link_pagamento',
            'data_criacao',
            'data_atualizacao',
        ]
        read_only_fields = [
            'status',
            'codigo_gateway',
            'link_pagamento',
            'data_criacao',
            'data_atualizacao',
        ]

    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "O valor da cobrança deve ser maior que zero."
            )
        return value
