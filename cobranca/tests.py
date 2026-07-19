from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from associados.models import Associado
from financeiro.models import PlanoDeContas

from .models import Cobranca
from .services import CobrancaService


User = get_user_model()


@override_settings(
    WEBHOOK_TOKEN="token-seguro-de-teste"
)
class CobrancaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="operador",
            password="password123",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.associado = Associado.objects.create(
            razao_social="Empresa Teste Ltda",
            cnpj="11222333000181",
            email="empresa@example.com",
            telefone="85999999999",
            endereco="Rua de Teste, 100",
            data_vencimento=(
                timezone.localdate()
                + timedelta(days=365)
            ),
        )

        self.plano = PlanoDeContas.objects.create(
            codigo="1.1",
            descricao="Mensalidades",
            tipo="RECEITA",
        )

        self.url_list = reverse(
            "cobrancas-list"
        )

        self.url_webhook = reverse(
            "webhook-pagamento"
        )

        self.payload_valido = {
            "associado": self.associado.id,
            "plano_conta": self.plano.id,
            "valor": "100.00",
            "descricao": "Mensalidade",
            "data_vencimento": (
                timezone.localdate()
                + timedelta(days=30)
            ).isoformat(),
        }

    def test_rota_de_cobrancas_funciona(self):
        response = self.client.get(
            self.url_list
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_criar_cobranca(self):
        response = self.client.post(
            self.url_list,
            self.payload_valido,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        cobranca = Cobranca.objects.get(
            pk=response.data["id"]
        )

        self.assertEqual(
            cobranca.associado,
            self.associado,
        )

        self.assertTrue(
            cobranca.codigo_gateway.startswith(
                "LOCAL-"
            )
        )

        self.assertEqual(
            cobranca.status,
            Cobranca.STATUS_PENDENTE,
        )

    def test_rejeitar_valor_negativo(self):
        payload = self.payload_valido.copy()
        payload["valor"] = "-10.00"

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
            "valor",
            response.data,
        )

    def test_filtrar_cobrancas_por_status(self):
        Cobranca.objects.create(
            associado=self.associado,
            plano_conta=self.plano,
            valor="50.00",
            descricao="Paga",
            data_vencimento=timezone.localdate(),
            codigo_gateway="CODIGO-PAGA",
            status=Cobranca.STATUS_PAGA,
        )

        Cobranca.objects.create(
            associado=self.associado,
            plano_conta=self.plano,
            valor="75.00",
            descricao="Pendente",
            data_vencimento=timezone.localdate(),
            codigo_gateway="CODIGO-PENDENTE",
            status=Cobranca.STATUS_PENDENTE,
        )

        response = self.client.get(
            self.url_list,
            {"status": Cobranca.STATUS_PAGA},
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
            response.data["results"][0]["status"],
            Cobranca.STATUS_PAGA,
        )

    def test_webhook_processa_pagamento(self):
        cobranca = Cobranca.objects.create(
            associado=self.associado,
            plano_conta=self.plano,
            valor="100.00",
            descricao="Pagamento via webhook",
            data_vencimento=timezone.localdate(),
            codigo_gateway="GATEWAY-123",
        )

        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.url_webhook,
            {
                "codigo_gateway": "GATEWAY-123",
                "status": "PAGA",
            },
            format="json",
            HTTP_X_WEBHOOK_TOKEN=(
                "token-seguro-de-teste"
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        cobranca.refresh_from_db()

        self.assertEqual(
            cobranca.status,
            Cobranca.STATUS_PAGA,
        )

    def test_webhook_rejeita_token_invalido(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.url_webhook,
            {
                "codigo_gateway": "QUALQUER",
                "status": "PAGA",
            },
            format="json",
            HTTP_X_WEBHOOK_TOKEN="token-incorreto",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_processamento_idempotente(self):
        cobranca = Cobranca.objects.create(
            associado=self.associado,
            plano_conta=self.plano,
            valor="100.00",
            descricao="Teste idempotente",
            data_vencimento=timezone.localdate(),
            codigo_gateway="IDEMPOTENTE-123",
        )

        CobrancaService.processar_pagamento_gateway(
            "IDEMPOTENTE-123"
        )

        resultado = (
            CobrancaService
            .processar_pagamento_gateway(
                "IDEMPOTENTE-123"
            )
        )

        cobranca.refresh_from_db()

        self.assertEqual(
            resultado.status,
            Cobranca.STATUS_PAGA,
        )

        self.assertEqual(
            cobranca.status,
            Cobranca.STATUS_PAGA,
        )

    def test_nao_pagar_cobranca_cancelada(self):
        Cobranca.objects.create(
            associado=self.associado,
            plano_conta=self.plano,
            valor="100.00",
            descricao="Cancelada",
            data_vencimento=timezone.localdate(),
            codigo_gateway="CANCELADA-123",
            status=Cobranca.STATUS_CANCELADA,
        )

        with self.assertRaises(ValidationError):
            (
                CobrancaService
                .processar_pagamento_gateway(
                    "CANCELADA-123"
                )
            )