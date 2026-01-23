from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from associados.models import Associado
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Verifica vencimentos e evita envios duplicados no mesmo dia'

    def handle(self, *args, **options):
        hoje = timezone.now().date()
        prazos = [7, 30]
        
        for dias in prazos:
            data_alvo = hoje + timedelta(days=dias)
            
            # Filtra por data de vencimento, status E garante que não enviou aviso HOJE
            associados = Associado.objects.filter(
                data_vencimento=data_alvo, 
                status='ATIVO'
            ).exclude(data_ultimo_aviso=hoje) # <-- Segurança extra

            if not associados.exists():
                self.stdout.write(f"Nenhum novo aviso para enviar em {dias} dias.")
                continue

            for asse in associados:
                self.enviar_email_alerta(asse, dias)
                
                # Marca que o aviso foi enviado hoje
                asse.data_ultimo_aviso = hoje
                asse.save(update_fields=['data_ultimo_aviso'])
                
                self.stdout.write(
                    self.style.SUCCESS(f'Alerta de {dias} dias enviado para: {asse.razao_social}')
                )

    def enviar_email_alerta(self, associado, dias):
        assunto = f'🔔 Lembrete: Vencimento em {dias} dias - {associado.razao_social}'
        mensagem = f"Olá, {associado.razao_social}.\nSeu contrato vence em {dias} dias ({associado.data_vencimento.strftime('%d/%m/%Y')})."
        email_de = getattr(settings, 'EMAIL_HOST_USER', 'sistema@apiaccg.com')
        
        send_mail(assunto, mensagem, email_de, [associado.email])