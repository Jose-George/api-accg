from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from cobranca.models import Cobranca


class AssociadoHistoricoService:
    @staticmethod
    def get_historico_associado(associado):
        cobrancas = (
            associado.cobrancas
            .select_related("plano_conta")
            .all()
        )

        total_pendente = (
            cobrancas
            .filter(
                status=Cobranca.STATUS_PENDENTE
            )
            .aggregate(total=Sum("valor"))
            .get("total")
            or Decimal("0.00")
        )

        total_pago = (
            cobrancas
            .filter(
                status=Cobranca.STATUS_PAGA
            )
            .aggregate(total=Sum("valor"))
            .get("total")
            or Decimal("0.00")
        )

        total_cancelado = (
            cobrancas
            .filter(
                status=Cobranca.STATUS_CANCELADA
            )
            .aggregate(total=Sum("valor"))
            .get("total")
            or Decimal("0.00")
        )

        ultimo_pagamento = (
            cobrancas
            .filter(
                status=Cobranca.STATUS_PAGA
            )
            .order_by("-data_atualizacao")
            .values_list(
                "data_atualizacao",
                flat=True,
            )
            .first()
        )

        possui_cobranca_atrasada = (
            cobrancas
            .filter(
                status=Cobranca.STATUS_PENDENTE,
                data_vencimento__lt=(
                    timezone.localdate()
                ),
            )
            .exists()
        )

        lista_cobrancas = []

        for cobranca in cobrancas:
            lista_cobrancas.append(
                {
                    "id": cobranca.id,
                    "descricao": cobranca.descricao,
                    "valor": cobranca.valor,
                    "status": cobranca.status,
                    "data_vencimento": (
                        cobranca.data_vencimento
                    ),
                    "codigo_gateway": (
                        cobranca.codigo_gateway
                    ),
                    "link_pagamento": (
                        cobranca.link_pagamento
                    ),
                    "plano_conta": {
                        "id": cobranca.plano_conta.id,
                        "codigo": (
                            cobranca.plano_conta.codigo
                        ),
                        "descricao": (
                            cobranca
                            .plano_conta
                            .descricao
                        ),
                    },
                    "data_criacao": (
                        cobranca.data_criacao
                    ),
                    "data_atualizacao": (
                        cobranca.data_atualizacao
                    ),
                }
            )

        eventos = [
            {
                "data": associado.data_cadastro,
                "tipo": "CADASTRO",
                "descricao": (
                    "Associado cadastrado no sistema."
                ),
            }
        ]

        for cobranca in cobrancas:
            eventos.append(
                {
                    "data": cobranca.data_criacao,
                    "tipo": "COBRANCA_CRIADA",
                    "descricao": (
                        f"Cobrança #{cobranca.id} "
                        f"criada no valor de "
                        f"R$ {cobranca.valor}."
                    ),
                }
            )

            if cobranca.status == Cobranca.STATUS_PAGA:
                eventos.append(
                    {
                        "data": (
                            cobranca.data_atualizacao
                        ),
                        "tipo": "PAGAMENTO",
                        "descricao": (
                            f"Cobrança #{cobranca.id} "
                            "marcada como paga."
                        ),
                    }
                )

        eventos.sort(
            key=lambda evento: evento["data"],
            reverse=True,
        )

        return {
            "associado": {
                "id": associado.id,
                "razao_social": (
                    associado.razao_social
                ),
                "nome_fantasia": (
                    associado.nome_fantasia
                ),
                "cnpj": associado.cnpj,
                "status": associado.status,
                "data_vencimento": (
                    associado.data_vencimento
                ),
            },
            "status_financeiro": {
                "total_pendente": total_pendente,
                "total_pago": total_pago,
                "total_cancelado": total_cancelado,
                "ultimo_pagamento": (
                    ultimo_pagamento
                ),
                "possui_cobranca_atrasada": (
                    possui_cobranca_atrasada
                ),
                "quantidade_cobrancas": (
                    cobrancas.count()
                ),
            },
            "cobrancas": lista_cobrancas,
            "eventos": eventos,
        }