from rest_framework import viewsets, filters
from .models import Associado
from .serializers import AssociadoSerializer 
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import AssociadoHistoricoService
from .serializers import AssociadoHistoricoSerializer, AssociadoSerializer

class AssociadoViewSet(viewsets.ModelViewSet):
    queryset = Associado.objects.all()
    serializer_class = AssociadoSerializer 

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['razao_social', 'cnpj', 'email']

    @action(detail=True, methods=['get'], url_path='historico')
    def historico(self, request, pk=None):
        # busca o associado atual
        associado = self.get_object() 
        
        # chama o serviço para consolidar os dados
        service = AssociadoHistoricoService()
        dados_historico = service.get_historico_associado(associado.id)
        
        # serializa e retorna
        serializer = AssociadoHistoricoSerializer(dados_historico)
        return Response(serializer.data)