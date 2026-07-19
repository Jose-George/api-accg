from django.contrib import admin

from .models import Associado


@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = [
        "razao_social",
        "cnpj",
        "data_vencimento",
        "status",
        "data_ultimo_aviso",
    ]

    list_filter = [
        "status",
        "data_vencimento",
    ]

    search_fields = [
        "razao_social",
        "nome_fantasia",
        "cnpj",
        "email",
    ]

    ordering = [
        "razao_social",
    ]

    readonly_fields = [
        "data_cadastro",
        "data_atualizacao",
        "data_ultimo_aviso",
    ]