from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Associado

class AssociadoModelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('associados-list') # Assumindo que o router criou essa rota
        self.valid_payload = {
             "razao_social": "Empresa Teste Ltda",
             "cnpj": "11.222.333/0001-81", # CNPJ Matematiamente Válido
             "email": "teste@empresa.com",
             "telefone": "11999999999",
             "endereco": "Rua Teste, 123"
        }

    def test_criar_associado_cnpj_valido(self):
        """
        Deve permitir cadastrar um associado com CNPJ válido.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            self.fail(f"Falha ao criar: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Associado.objects.count(), 1)
        self.assertEqual(Associado.objects.get().cnpj, "11222333000181") # Serializer limpa a pontuação

    def test_nao_criar_associado_cnpj_invalido_digito(self):
        """
        Deve rejeitar CNPJ com dígitos verificadores errados.
        """
        payload = self.valid_payload.copy()
        payload['cnpj'] = "92.352.308/0001-99" # Dígitos errados
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cnpj', response.data)
        self.assertIn('erro de verificação', str(response.data['cnpj'][0]))

    def test_nao_criar_associado_cnpj_repetido(self):
        """
        Deve rejeitar CNPJ com dígitos repetidos.
        """
        payload = self.valid_payload.copy()
        payload['cnpj'] = "00.000.000/0000-00"
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dígitos repetidos', str(response.data['cnpj'][0]))

    def test_nao_criar_associado_cnpj_tamanho_invalido(self):
        """
        Deve rejeitar CNPJ com tamanho incorreto.
        """
        payload = self.valid_payload.copy()
        payload['cnpj'] = "12345" 
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
