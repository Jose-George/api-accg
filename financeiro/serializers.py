from rest_framework import serializers

from .models import PlanoDeContas


class PlanoDeContasSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PlanoDeContas
        fields = [
            "id",
            "codigo",
            "descricao",
            "tipo",
            "categoria",
            "ativo",
            "observacoes",
            "data_cadastro",
            "data_atualizacao",
        ]
        read_only_fields = [
            "id",
            "data_cadastro",
            "data_atualizacao",
        ]
        extra_kwargs = {
            "codigo": {
                "validators": [],
            },
        }

    def validate_codigo(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O código não pode ficar vazio."
            )

        queryset = PlanoDeContas.objects.filter(
            codigo=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Já existe um plano de contas "
                "com este código."
            )

        return value

    def validate_descricao(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A descrição não pode ficar vazia."
            )

        return value