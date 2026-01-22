from rest_framework import serializers # Importação necessária
from .utils import validar_cpf, validar_cnpj

class AssociadoService:
    @staticmethod
    def validar_documento(tipo_pessoa, documento):
        if tipo_pessoa == 'PF':
            if not validar_cpf(documento):
                # Trocamos ValueError por ValidationError
                raise serializers.ValidationError({"documento": "CPF inválido."})
        elif tipo_pessoa == 'PJ':
            if not validar_cnpj(documento):
                # Trocamos ValueError por ValidationError
                raise serializers.ValidationError({"documento": "CNPJ inválido."})
        return True