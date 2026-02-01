from django.test import TestCase
from unittest.mock import MagicMock
from django.core.exceptions import ValidationError
from .services import CobrancaService
from .models import Cobranca

class CobrancaServiceTests(TestCase):
    def setUp(self):
        # Setup básico (mock ou real models)
        # Como estamos testando o service que usa ORM, podemos usar o BD de teste
        # mas aqui vamos criar objetos reais para simplificar
        from financeiro.models import PlanoDeContas
        self.plano = PlanoDeContas.objects.create(
            codigo="1.1", 
            descricao="Receita", 
            tipo="RECEITA"
        )
        self.cobranca = Cobranca.objects.create(
            plano_conta=self.plano,
            valor=100.00,
            descricao="Teste Pagamento",
            data_vencimento="2024-01-01",
            codigo_gateway="GATEWAY_123",
            status="PENDENTE"
        )

    def test_processar_pagamento_sucesso(self):
        """Deve baixar a cobrança corretamente"""
        updated_cobranca = CobrancaService.processar_pagamento_gateway("GATEWAY_123")
        self.cobranca.refresh_from_db()
        
        self.assertEqual(updated_cobranca.status, 'PAGA')
        self.assertEqual(self.cobranca.status, 'PAGA')

    def test_processar_pagamento_idempotente(self):
        """Deve lidar com múltiplas chamadas sem erro"""
        # Primeira chamada
        CobrancaService.processar_pagamento_gateway("GATEWAY_123")
        
        # Segunda chamada
        updated_cobranca = CobrancaService.processar_pagamento_gateway("GATEWAY_123")
        self.assertEqual(updated_cobranca.status, 'PAGA')

    def test_erro_pagar_cobranca_cancelada(self):
        """Não deve permitir pagar cobrança cancelada"""
        self.cobranca.status = 'CANCELADA'
        self.cobranca.save()
        
        with self.assertRaises(ValidationError):
            CobrancaService.processar_pagamento_gateway("GATEWAY_123")
            
    def test_erro_cobranca_inexistente(self):
        """Deve levantar erro se código não existe"""
        with self.assertRaises(ValidationError):
            CobrancaService.processar_pagamento_gateway("CODIGO_INEXISTENTE")
