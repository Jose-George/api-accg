from rest_framework import serializers
from .models import Associado
import re

class AssociadoSerializer(serializers.ModelSerializer):

    cnpj = serializers.CharField(max_length=18)

    class Meta:
        model = Associado
        fields = '__all__'
        # data_vencimento como leitura apenas
        read_only_fields = ['data_vencimento']
        
    def validate_cnpj(self, value):
        cnpj_limpo = re.sub(r'[^0-9]', '', value)
        
        # se não tiver 14 dígitos, o Django DEVE retornar erro 400
        if len(cnpj_limpo) != 14:
            raise serializers.ValidationError(f"CNPJ inválido! Recebemos {len(cnpj_limpo)} dígitos, mas precisamos de 14.")
            
        return cnpj_limpo
    
class AssociadoHistoricoSerializer(serializers.Serializer):
    associado = serializers.DictField()
    status_financeiro = serializers.DictField()
    pagamentos = serializers.ListField()
    faturas = serializers.ListField()
    eventos = serializers.ListField()