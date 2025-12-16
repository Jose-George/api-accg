from django.db import models

class Associado(models.Model):
    id = models.AutoField(primary_key=True) # Campo de chave primária automática
    razao_social = models.CharField(max_length=255, help_text="Razão Social do associado") # Campo de texto
    nome_fantasia = models.CharField(max_length=255, help_text="Nome do associado") # Campo de texto
    cnpj = models.CharField(max_length=14, unique=True, help_text="CNPJ máximo 14 caracteres") # Campo de texto único
    email = models.EmailField(unique=True, help_text="Email do associado") # Campo de email único
    telefone = models.CharField(max_length=20, help_text="Telefone do associado") # Campo de texto
    endereco = models.TextField(help_text="Endereço completo do associado") # Campo de texto longo
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True, help_text="Arquivo do contrato") # Campo de arquivo
    ficha_cadastral = models.FileField(upload_to='fichas/', null=True, blank=True, help_text="Arquivo da ficha cadastral") # Campo de arquivo
    data_vencimento = models.DateField(help_text="Data de vencimento do associado")
    status = {
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('SUSPENSO', 'Suspenso'),
    }
    status = models.CharField(max_length=10, choices=status, default='ATIVO', help_text="Status do associado") # Campo com escolhas predefinidas
    data_cadastro = models.DateTimeField(auto_now_add=True, help_text="Data de cadastro do associado") # Data e hora de criação automática
    data_atualizacao = models.DateTimeField(auto_now=True, help_text="Data de atualização do associado") # Data e hora de atualização automática

def save(self, *args, **kwargs):
    if not self.pk:  # Se for criação (novo registro)
        # Define vencimento para 1 ano a partir de hoje
        from datetime import date, timedelta
        self.data_vencimento = date.today() + timedelta(days=365)
    super().save(*args, **kwargs)

    def __str__(self): 
        return self.nome
   