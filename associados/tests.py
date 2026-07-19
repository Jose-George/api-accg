from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import (
    TestCase,
    override_settings,
)
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from cobranca.models import Cobranca
from financeiro.models import PlanoDeContas

from .models import Associado


User = get_user_model()


class AssociadoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="operador",
            password="password123",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.url = reverse(
            "associados-list"
        )

        self.valid_payload = {
            "razao_social": "Empresa Teste Ltda",
            "nome_fantasia": "Empresa Teste",
            "cnpj": "11.222.333/0001-81",
            "email": "teste@empresa.com",
            "telefone": "11999999999",
            "endereco": "Rua Teste, 123",
        }

    def test_criar_associado_com_cnpj_valido(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )

        associado = Associado.objects.get()

        self.assertEqual(
            associado.cnpj,
            "11222333000181",
        )

        self.assertIsNotNone(
            associado.data_vencimento
        )

    def test_rejeitar_cnpj_invalido(self):
        payload = self.valid_payload.copy()
        payload["cnpj"] = "92.352.308/0001-99"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "cnpj",
            response.data,
        )

    def test_rejeitar_cnpj_repetido(self):
        payload = self.valid_payload.copy()
        payload["cnpj"] = "00.000.000/0000-00"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_rejeitar_cnpj_duplicado(self):
        self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "cnpj",
            response.data,
        )

    def test_endpoint_exige_autenticacao(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_historico_retorna_cobrancas_reais(self):
        associado = Associado.objects.create(
            razao_social="Histórico Ltda",
            cnpj="11444777000161",
            email="historico@example.com",
            telefone="85999999999",
            endereco="Rua do Histórico",
            data_vencimento=(
                timezone.localdate()
                + timedelta(days=365)
            ),
        )

        plano = PlanoDeContas.objects.create(
            codigo="1.10",
            descricao="Mensalidade",
            tipo="RECEITA",
        )

        Cobranca.objects.create(
            associado=associado,
            plano_conta=plano,
            valor="75.00",
            descricao="Cobrança paga",
            data_vencimento=timezone.localdate(),
            codigo_gateway="HIST-PAGA",
            status=Cobranca.STATUS_PAGA,
        )

        Cobranca.objects.create(
            associado=associado,
            plano_conta=plano,
            valor="25.00",
            descricao="Cobrança pendente",
            data_vencimento=(
                timezone.localdate()
                + timedelta(days=5)
            ),
            codigo_gateway="HIST-PENDENTE",
            status=Cobranca.STATUS_PENDENTE,
        )

        url = reverse(
            "associados-historico",
            args=[associado.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["cobrancas"]),
            2,
        )

        self.assertEqual(
            str(
                response.data[
                    "status_financeiro"
                ]["total_pago"]
            ),
            "75.00",
        )

        self.assertEqual(
            str(
                response.data[
                    "status_financeiro"
                ]["total_pendente"]
            ),
            "25.00",
        )


@override_settings(
    EMAIL_BACKEND=(
        "django.core.mail.backends."
        "locmem.EmailBackend"
    ),
    DEFAULT_FROM_EMAIL="sistema@example.com",
)
class AlertaVencimentoCommandTest(TestCase):
    def setUp(self):
        self.associado = Associado.objects.create(
            razao_social="Empresa Alerta Ltda",
            cnpj="07422853000103",
            email="alerta@example.com",
            telefone="85999999999",
            endereco="Rua dos Alertas",
            data_vencimento=(
                timezone.localdate()
                + timedelta(days=7)
            ),
        )

    def test_enviar_aviso_sem_duplicar(self):
        call_command(
            "check_vencimentos",
            "--dias",
            "7",
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        self.associado.refresh_from_db()

        self.assertEqual(
            self.associado.data_ultimo_aviso,
            timezone.localdate(),
        )

        call_command(
            "check_vencimentos",
            "--dias",
            "7",
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )