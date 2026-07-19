import re

from rest_framework import serializers

from .models import Associado


class AssociadoSerializer(serializers.ModelSerializer):
    cnpj = serializers.CharField(
        max_length=18,
    )

    class Meta:
        model = Associado
        fields = [
            "id",
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "email",
            "telefone",
            "endereco",
            "contrato",
            "ficha_cadastral",
            "data_vencimento",
            "status",
            "data_cadastro",
            "data_atualizacao",
            "data_ultimo_aviso",
        ]
        read_only_fields = [
            "id",
            "data_vencimento",
            "data_cadastro",
            "data_atualizacao",
            "data_ultimo_aviso",
        ]

    def validate_cnpj(self, value):
        cnpj = re.sub(r"[^0-9]", "", value)

        if len(cnpj) != 14:
            raise serializers.ValidationError(
                "O CNPJ deve ter exatamente 14 dígitos."
            )

        if len(set(cnpj)) == 1:
            raise serializers.ValidationError(
                "CNPJ inválido: todos os dígitos são iguais."
            )

        if not self._validar_digitos_cnpj(cnpj):
            raise serializers.ValidationError(
                "CNPJ inválido: erro nos dígitos verificadores."
            )

        queryset = Associado.objects.filter(
            cnpj=cnpj
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Já existe um associado com este CNPJ."
            )

        return cnpj

    @staticmethod
    def _validar_digitos_cnpj(cnpj):
        primeiro_peso = [
            5, 4, 3, 2, 9, 8,
            7, 6, 5, 4, 3, 2,
        ]

        segundo_peso = [
            6, 5, 4, 3, 2, 9, 8,
            7, 6, 5, 4, 3, 2,
        ]

        primeiros_digitos = [
            int(digito)
            for digito in cnpj[:12]
        ]

        soma = sum(
            numero * peso
            for numero, peso in zip(
                primeiros_digitos,
                primeiro_peso,
            )
        )

        resto = soma % 11
        primeiro_verificador = (
            0 if resto < 2 else 11 - resto
        )

        numeros_com_primeiro = (
            primeiros_digitos
            + [primeiro_verificador]
        )

        soma = sum(
            numero * peso
            for numero, peso in zip(
                numeros_com_primeiro,
                segundo_peso,
            )
        )

        resto = soma % 11
        segundo_verificador = (
            0 if resto < 2 else 11 - resto
        )

        return (
            primeiro_verificador
            == int(cnpj[12])
            and segundo_verificador
            == int(cnpj[13])
        )


class AssociadoHistoricoSerializer(
    serializers.Serializer
):
    associado = serializers.DictField()
    status_financeiro = serializers.DictField()

    cobrancas = serializers.ListField(
        child=serializers.DictField()
    )

    eventos = serializers.ListField(
        child=serializers.DictField()
    )