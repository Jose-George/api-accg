from rest_framework import serializers
from .models import Associado

class AssociadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Associado
        fields = '__all__'
        # data_vencimento como leitura apenas
        read_only_fields = ['data_vencimento']