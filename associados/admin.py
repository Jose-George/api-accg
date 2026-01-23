from django.contrib import admin
from .models import Associado

@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'data_vencimento', 'status', 'data_ultimo_aviso')
    list_filter = ('status', 'data_vencimento')