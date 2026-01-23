from django.db import models
from datetime import date, timedelta

class Associado(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('SUSPENSO', 'Suspenso'),
    ]

    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    
    # uploads de ficheiros
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)
    ficha_cadastral = models.FileField(upload_to='fichas/', null=True, blank=True)
    
    # datas
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # salva o ultimo email de aviso evitando envios duplicados
    data_ultimo_aviso = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.data_vencimento = date.today() + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.razao_social