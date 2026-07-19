# Fazer testes programaticos do comando de envio de email 7 dias antes do vencimento

from associados.models import Associado
from datetime import date, timedelta
from django.core.management import call_command

# 1. Criar (ou atualizar) um associado para teste
# vencimento para exatamente daqui a 7 dias
data_teste = date.today() + timedelta(days=7)
email_destino = 'kaymmiknb@gmail.com' # E-mail pessoal para testes

obj, created = Associado.objects.update_or_create(
    cnpj="99999999000199",
    defaults={
        'razao_social': "Empresa de Teste Real",
        'email': email_destino,
        'data_vencimento': data_teste,
        'status': 'ATIVO',
        'data_ultimo_aviso': None # Limpamos para garantir que o script envie
    }
)

print(f"Associado pronto: {obj.razao_social} | Vencimento: {obj.data_vencimento}")

# 2. Chamar o comando de envio programaticamente
print("Disparando comando de verificação...")
call_command('check_vencimentos')