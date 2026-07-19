from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PlanoDeContas
from .serializers import PlanoDeContasSerializer


class PlanoDeContasViewSet(
    viewsets.ModelViewSet
):
    queryset = PlanoDeContas.objects.filter(
        ativo=True
    )

    serializer_class = PlanoDeContasSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "tipo",
        "categoria",
    ]

    search_fields = [
        "codigo",
        "descricao",
        "categoria",
    ]

    ordering_fields = [
        "codigo",
        "descricao",
        "tipo",
        "categoria",
        "data_cadastro",
    ]

    ordering = [
        "codigo",
    ]

    def perform_destroy(self, instance):
        instance.ativo = False
        instance.save(
            update_fields=[
                "ativo",
                "data_atualizacao",
            ]
        )