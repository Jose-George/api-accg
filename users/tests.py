from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        """Deve criar um usuário com sucesso"""
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Cria um usuário para autenticação
        self.user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        self.client.force_authenticate(user=self.user)
        self.url = '/api/users/' # Ajuste conforme a rota real do DefaultRouter

    def test_list_users_authenticated(self):
        """Usuário autenticado deve conseguir listar usuários"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_unauthenticated(self):
        """Usuário não autenticado deve ter acesso negado (Devido ao IsAuthenticated global)"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertTrue(response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
