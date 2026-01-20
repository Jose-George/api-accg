from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cobranca

class WebhookPagamentoView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        codigo_gateway = request.data.get('codigo_gateway')
        status_pagamento = request.data.get('status')

        if not codigo_gateway or not status_pagamento:
            return Response(
                {"erro": "Dados obrigatórios não informados"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cobranca = Cobranca.objects.get(codigo_gateway=codigo_gateway)
        except Cobranca.DoesNotExist:
            return Response(
                {"erro": "Cobrança não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        if status_pagamento == 'PAGA':
            cobranca.status = 'PAGA'
            cobranca.save()

        return Response(
            {"mensagem": "Status da cobrança atualizado com sucesso"},
            status=status.HTTP_200_OK
        )
