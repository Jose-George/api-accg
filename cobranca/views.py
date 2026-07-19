from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cobranca
from .serializers import CobrancaSerializer
from .services import CobrancaService


class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = (
        Cobranca.objects
        .select_related(
            "associado",
            "plano_conta",
        )
        .all()
    )

    serializer_class = CobrancaSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "associado",
        "plano_conta",
        "data_vencimento",
    ]

    search_fields = [
        "descricao",
        "codigo_gateway",
        "associado__razao_social",
        "associado__cnpj",
        "plano_conta__codigo",
        "plano_conta__descricao",
    ]

    ordering_fields = [
        "data_criacao",
        "data_vencimento",
        "valor",
        "status",
    ]

    ordering = ["-data_criacao"]

    def perform_create(self, serializer):
        serializer.save(
            codigo_gateway=(
                CobrancaService.gerar_codigo_gateway()
            )
        )