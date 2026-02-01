from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from decouple import config
from .services import CobrancaService

class WebhookPagamentoView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # 1. Segurança: Verificar Token
        token_recebido = request.headers.get('X-Webhook-Token')
        token_esperado = config('WEBHOOK_TOKEN', default=None)
        
        if not token_esperado or token_recebido != token_esperado:
             return Response(
                {"erro": "Acesso não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Validação de Entrada
        codigo_gateway = request.data.get('codigo_gateway')
        status_pagamento = request.data.get('status')

        if not codigo_gateway or not status_pagamento:
            return Response(
                {"erro": "Dados obrigatórios não informados"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Processamento via Service Layer
        if status_pagamento == 'PAGA':
            try:
                CobrancaService.processar_pagamento_gateway(codigo_gateway)
            except ValidationError as e:
                return Response(
                    {"erro": str(e)}, # .message
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception:
                 return Response(
                    {"erro": "Erro interno ao processar pagamento"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"mensagem": "Evento processado com sucesso"},
            status=status.HTTP_200_OK
        )
