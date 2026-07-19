from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Associado
from .serializers import (
    AssociadoHistoricoSerializer,
    AssociadoSerializer,
)
from .services import AssociadoHistoricoService


class AssociadoViewSet(viewsets.ModelViewSet):
    queryset = Associado.objects.all()
    serializer_class = AssociadoSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "razao_social",
        "nome_fantasia",
        "cnpj",
        "email",
    ]

    ordering_fields = [
        "razao_social",
        "data_cadastro",
        "data_vencimento",
        "status",
    ]

    ordering = ["razao_social"]

    @action(
        detail=True,
        methods=["get"],
        url_path="historico",
    )
    def historico(self, request, pk=None):
        associado = self.get_object()

        dados = (
            AssociadoHistoricoService
            .get_historico_associado(
                associado
            )
        )

        serializer = AssociadoHistoricoSerializer(
            instance=dados
        )

        return Response(serializer.data)