from django.contrib import admin
from .models import Associado

@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'data_vencimento', 'status', 'data_ultimo_aviso')
    list_filter = ('status', 'data_vencimento')

from associados.models import Associado
from datetime import date, timedelta
from django.core.management import call_command
