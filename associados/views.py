from rest_framework import viewsets
from .models import Associado
from .serializers import AssociadoSerializer

class AssociadoViewSet(viewsets.ModelViewSet):
    queryset = Associado.objects.all()
    serializer_class = AssociadoSerializer