from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Garante que apenas administradores do sistema gerenciem usuários
    permission_classes = [IsAuthenticated, IsAdminUser]