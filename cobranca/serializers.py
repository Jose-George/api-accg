from django.utils import timezone
from rest_framework import serializers

from associados.models import Associado

from .models import Cobranca


class CobrancaSerializer(serializers.ModelSerializer):
    associado = serializers.PrimaryKeyRelatedField(
        queryset=Associado.objects.all(),
        required=True,
    )

    associado_nome = serializers.CharField(
        source="associado.razao_social",
        read_only=True,
    )

    plano_conta_descricao = serializers.CharField(
        source="plano_conta.descricao",
        read_only=True,
    )

    class Meta:
        model = Cobranca
        fields = [
            "id",
            "associado",
            "associado_nome",
            "plano_conta",
            "plano_conta_descricao",
            "valor",
            "descricao",
            "status",
            "data_vencimento",
            "codigo_gateway",
            "link_pagamento",
            "data_criacao",
            "data_atualizacao",
        ]
        read_only_fields = [
            "id",
            "status",
            "codigo_gateway",
            "link_pagamento",
            "data_criacao",
            "data_atualizacao",
        ]

    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "O valor da cobrança deve ser maior que zero."
            )

        return value

    def validate_data_vencimento(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError(
                "A data de vencimento não pode estar no passado."
            )

        return value

    def validate_plano_conta(self, value):
        if not value.ativo:
            raise serializers.ValidationError(
                "Não é possível utilizar um plano de contas inativo."
            )

        return value