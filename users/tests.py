from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        self.assertEqual(
            user.username,
            "testuser",
        )
        self.assertTrue(
            user.check_password("password123")
        )
        self.assertTrue(user.is_active)


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            username="admin",
            password="password123",
            email="admin@example.com",
        )

        self.usuario_comum = User.objects.create_user(
            username="comum",
            password="password123",
        )

        self.url = reverse("users-list")

    def test_admin_pode_listar_usuarios(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_usuario_comum_nao_pode_listar(self):
        self.client.force_authenticate(
            user=self.usuario_comum
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_usuario_nao_autenticado_nao_pode_listar(
        self
    ):
        response = self.client.get(self.url)

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_admin_cria_usuario_com_senha_criptografada(
        self
    ):
        self.client.force_authenticate(
            user=self.admin
        )

        payload = {
            "username": "novo_usuario",
            "first_name": "Novo",
            "last_name": "Usuário",
            "email": "novo@example.com",
            "password": "senha-segura-123",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        usuario = User.objects.get(
            username="novo_usuario"
        )

        self.assertTrue(
            usuario.check_password(
                "senha-segura-123"
            )
        )

        self.assertNotIn(
            "password",
            response.data,
        )