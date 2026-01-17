#from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import PlanoDeContas
from .serializers import PlanoDeContasSerializer

class PlanoDeContasViewSet(viewsets.ModelViewSet):
    queryset = PlanoDeContas.objects.filter(ativo=True)
    serializer_class = PlanoDeContasSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        'codigo',
        'descricao',
        'categoria',
    ]

    ordering_fields = [
        'codigo',
        'descricao',
        'tipo',
    ]

    filterset_fields = [
        'tipo',
        'ativo',
        'categoria',
    ]

    def perform_destroy(self, instance):
        instance.ativo = False
        instance.save()
