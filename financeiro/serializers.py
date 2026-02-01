from rest_framework import serializers
from .models import PlanoDeContas

class PlanoDeContasSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanoDeContas
        fields = [
            'id',
            'codigo',
            'descricao',
            'tipo',
            'categoria',
            'ativo',
            'observacoes',
            'data_cadastro',
            'data_atualizacao',
        ]

    def validate_codigo(self, value):
        if self.instance is None:
            if PlanoDeContas.objects.filter(codigo=value).exists():
                raise serializers.ValidationError("Código já existe")
        return value

    def validate_tipo(self, value):

        tipos_validos = dict(self.Meta.model.TIPO_CHOICES).keys()

        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo deve ser um dos seguintes: {', '.join(tipos_validos)}"
            )
        return value


