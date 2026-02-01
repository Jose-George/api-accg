from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import PlanoDeContas

User = get_user_model()

class PlanoDeContasTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='admin', password='password123')
        self.client.force_authenticate(user=self.user)
        
        self.plano = PlanoDeContas.objects.create(
            codigo="1.0",
            descricao="Receitas Gerais",
            tipo="RECEITA",
            ativo=True
        )
        self.url_list = '/api/planos-contas/'
        self.url_detail = f'/api/planos-contas/{self.plano.id}/'

    def test_soft_delete_comportamento(self):
        """Ao deletar, o registro deve permanecer no banco mas como inativo"""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se o objeto ainda existe no banco
        self.plano.refresh_from_db()
        self.assertFalse(self.plano.ativo, "O campo 'ativo' deveria ser False após o delete")
        self.assertEqual(PlanoDeContas.objects.count(), 1, "O registro não deveria ser removido fisicamente")

    def test_listagem_filtra_inativos(self):
        """A listagem padrão não deve exibir itens inativos"""
        # Torna inativo manualmente
        self.plano.ativo = False
        self.plano.save()
        
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0, "Itens inativos não devem aparecer na listagem")

    def test_criar_plano_contas(self):
        """Teste básico de criação"""
        payload = {
            "codigo": "2.0",
            "descricao": "Despesas",
            "tipo": "DESPESA"
        }
        response = self.client.post(self.url_list, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
