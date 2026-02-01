from .models import Associado

class AssociadoHistoricoService:
    @staticmethod
    def get_historico_associado(associado_id):
        try:
            associado = Associado.objects.get(id=associado_id)
            
            historico = {
                'associado': {
                    'id': associado.id,
                    'razao_social': associado.razao_social,
                    'cnpj': associado.cnpj,
                    'status': associado.status,
                    'data_vencimento': associado.data_vencimento,
                },
                'status_financeiro': {
                    'total_pendente': 0.0,
                    'total_pago': 0.0,
                    'ultimo_pagamento': None,
                },
                'pagamentos': [],  # Pagamento.objects.filter(...)
                'faturas': [],     # Fatura.objects.filter(...)
                'eventos': [
                    {"data": associado.data_cadastro, "descricao": "Cadastro realizado no sistema"}
                ],
            }
            return historico
        except Associado.DoesNotExist:
            return None