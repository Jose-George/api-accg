from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Cobranca
from .serializers import CobrancaSerializer

class CobrancaViewSet(viewsets.ModelViewSet):

    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        'descricao',
        'plano_conta__codigo',
        'plano_conta__descricao',
    ]

    ordering_fields = [
        'data_vencimento',
        'valor',
        'status',
    ]

    filterset_fields = [
        'status',
        'plano_conta',
    ]

    def perform_create(self, serializer):

        cobranca = serializer.save()
        # integração com gateway bota aqui
        return cobranca
