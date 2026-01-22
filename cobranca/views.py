from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend 
from .models import Cobranca
from .serializers import CobrancaSerializer

class CobrancaViewSet(viewsets.ModelViewSet):
    # Otimização com select_related
    queryset = Cobranca.objects.select_related('associado', 'plano_conta').all()
    serializer_class = CobrancaSerializer
    
    # Corrigindo os filtros 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'plano_conta']
    search_fields = ['nosso_numero', 'codigo_gateway']