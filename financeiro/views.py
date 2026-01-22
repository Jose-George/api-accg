from rest_framework import viewsets, response, status
from .models import PlanoDeContas
from .serializers import PlanoDeContasSerializer

class PlanoDeContasViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoDeContasSerializer

    def get_queryset(self):
        # Para listagem (GET /api/financeiro/plano-de-contas/), mostra apenas ativos
        if self.action == 'list':
            return PlanoDeContas.objects.filter(ativo=True)
        # Para detalhes, edições ou exclusões, permite acessar os inativos
        return PlanoDeContas.objects.all()

    def destroy(self, request, *args, **kwargs):
        # Soft Delete: Em vez de apagar, desativa
        instance = self.get_object()
        instance.ativo = False
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)