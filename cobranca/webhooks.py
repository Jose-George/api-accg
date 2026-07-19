import logging
from secrets import compare_digest

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cobranca
from .services import CobrancaService


logger = logging.getLogger(__name__)


class WebhookPagamentoView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token_recebido = request.headers.get(
            "X-Webhook-Token",
            "",
        )

        token_esperado = settings.WEBHOOK_TOKEN

        if (
            not token_esperado
            or not compare_digest(
                token_recebido,
                token_esperado,
            )
        ):
            return Response(
                {"erro": "Acesso não autorizado."},
                status=status.HTTP_403_FORBIDDEN,
            )

        codigo_gateway = request.data.get(
            "codigo_gateway"
        )

        status_pagamento = str(
            request.data.get("status", "")
        ).strip().upper()

        if not codigo_gateway:
            return Response(
                {
                    "erro": (
                        "O campo codigo_gateway é obrigatório."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if status_pagamento != Cobranca.STATUS_PAGA:
            return Response(
                {
                    "erro": (
                        "O webhook aceita apenas o status PAGA."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cobranca = (
                CobrancaService
                .processar_pagamento_gateway(
                    codigo_gateway
                )
            )
        except ValidationError as exc:
            mensagem = (
                exc.messages[0]
                if hasattr(exc, "messages")
                else str(exc)
            )

            return Response(
                {"erro": mensagem},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception(
                "Erro inesperado ao processar webhook."
            )

            return Response(
                {
                    "erro": (
                        "Erro interno ao processar pagamento."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "mensagem": (
                    "Evento processado com sucesso."
                ),
                "cobranca_id": cobranca.id,
                "status": cobranca.status,
            },
            status=status.HTTP_200_OK,
        )