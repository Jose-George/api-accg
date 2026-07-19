from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import PlanoDeContas


User = get_user_model()


class PlanoDeContasTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="admin",
            password="password123",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.plano = PlanoDeContas.objects.create(
            codigo="1.0",
            descricao="Receitas Gerais",
            tipo="RECEITA",
            categoria="Receitas",
            ativo=True,
        )

        self.url_list = reverse(
            "planos-contas-list"
        )

        self.url_detail = reverse(
            "planos-contas-detail",
            args=[self.plano.id],
        )

    def test_soft_delete(self):
        response = self.client.delete(
            self.url_detail
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.plano.refresh_from_db()

        self.assertFalse(self.plano.ativo)

        self.assertEqual(
            PlanoDeContas.objects.count(),
            1,
        )

    def test_listagem_nao_exibe_inativos(self):
        self.plano.ativo = False
        self.plano.save()

        response = self.client.get(
            self.url_list
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            0,
        )

    def test_criar_plano_de_contas(self):
        payload = {
            "codigo": "2.0",
            "descricao": "Despesas Gerais",
            "tipo": "DESPESA",
            "categoria": "Despesas",
        }

        response = self.client.post(
            self.url_list,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_filtrar_plano_por_tipo(self):
        PlanoDeContas.objects.create(
            codigo="2.0",
            descricao="Despesas Gerais",
            tipo="DESPESA",
            categoria="Despesas",
        )

        response = self.client.get(
            self.url_list,
            {"tipo": "DESPESA"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            response.data["results"][0]["tipo"],
            "DESPESA",
        )

    def test_rejeitar_codigo_duplicado(self):
        payload = {
            "codigo": "1.0",
            "descricao": "Outra conta",
            "tipo": "RECEITA",
        }

        response = self.client.post(
            self.url_list,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "codigo",
            response.data,
        )