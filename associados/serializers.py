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
        cnpj = re.sub(r'[^0-9]', '', value)
        
        if len(cnpj) != 14:
            raise serializers.ValidationError("O CNPJ deve ter exatamente 14 dígitos.")
            
        # Verifica se todos os dígitos são iguais (ex: 00000000000000)
        if len(set(cnpj)) == 1:
            raise serializers.ValidationError("CNPJ inválido (dígitos repetidos).")

        # Validação do primeiro dígito verificador
        tamanho = 12
        numeros = cnpj[:tamanho]
        digitos = cnpj[tamanho:]
        soma = 0
        pos = tamanho - 7
        for i in range(tamanho, 0, -1):
            soma += int(numeros[tamanho - i]) * pos
            pos -= 1
            if pos < 2:
                pos = 9
        
        resultado = soma % 11
        if resultado < 2:
            digito_1 = 0
        else:
            digito_1 = 11 - resultado

        if digito_1 != int(digitos[0]):
            raise serializers.ValidationError("CNPJ inválido (erro de verificação).")

        # Validação do segundo dígito verificador
        tamanho = 13
        numeros = cnpj[:tamanho]
        soma = 0
        pos = tamanho - 7
        for i in range(tamanho, 0, -1):
            soma += int(numeros[tamanho - i]) * pos
            pos -= 1
            if pos < 2:
                pos = 9

        resultado = soma % 11
        if resultado < 2:
            digito_2 = 0
        else:
            digito_2 = 11 - resultado

        if digito_2 != int(digitos[1]):
             raise serializers.ValidationError("CNPJ inválido (erro de verificação).")
            
        return cnpj
    
class AssociadoHistoricoSerializer(serializers.Serializer):
    associado = serializers.DictField()
    status_financeiro = serializers.DictField()
    pagamentos = serializers.ListField()
    faturas = serializers.ListField()
    eventos = serializers.ListField()