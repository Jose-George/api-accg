from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from associados.models import Associado


class Command(BaseCommand):
    help = (
        "Verifica contratos próximos do vencimento "
        "e envia os avisos por e-mail."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dias",
            nargs="+",
            type=int,
            default=[30, 7],
            help=(
                "Prazos, em dias, para envio dos avisos. "
                "Exemplo: --dias 30 7"
            ),
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=(
                "Mostra os avisos que seriam enviados, "
                "sem enviar e-mails."
            ),
        )

    def handle(self, *args, **options):
        hoje = timezone.localdate()
        prazos = sorted(
            set(options["dias"]),
            reverse=True,
        )
        dry_run = options["dry_run"]

        total_enviado = 0

        for dias in prazos:
            data_alvo = hoje + timedelta(days=dias)

            associados = (
                Associado.objects
                .filter(
                    data_vencimento=data_alvo,
                    status=Associado.STATUS_ATIVO,
                )
                .exclude(
                    data_ultimo_aviso=hoje
                )
                .order_by("razao_social")
            )

            if not associados.exists():
                self.stdout.write(
                    f"Nenhum novo aviso para {dias} dias."
                )
                continue

            for associado in associados:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            "[SIMULAÇÃO] "
                            f"{associado.razao_social} - "
                            f"{associado.email} - "
                            f"vence em {dias} dias."
                        )
                    )
                    continue

                quantidade = self.enviar_email_alerta(
                    associado=associado,
                    dias=dias,
                )

                if quantidade:
                    associado.data_ultimo_aviso = hoje
                    associado.save(
                        update_fields=[
                            "data_ultimo_aviso",
                            "data_atualizacao",
                        ]
                    )

                    total_enviado += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Aviso enviado para "
                            f"{associado.razao_social}."
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"O e-mail de "
                            f"{associado.razao_social} "
                            "não foi enviado."
                        )
                    )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "Simulação concluída. "
                    "Nenhum e-mail foi enviado."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Processamento concluído. "
                    f"{total_enviado} aviso(s) enviado(s)."
                )
            )

    @staticmethod
    def enviar_email_alerta(associado, dias):
        assunto = (
            f"Lembrete de vencimento em {dias} dias - "
            f"{associado.razao_social}"
        )

        mensagem = (
            f"Olá, {associado.razao_social}.\n\n"
            f"O contrato cadastrado na ACCG vence em "
            f"{dias} dias, na data "
            f"{associado.data_vencimento:%d/%m/%Y}.\n\n"
            "Entre em contato para obter mais informações."
        )

        return send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[associado.email],
            fail_silently=False,
        )