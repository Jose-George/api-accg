# API de Gerenciamento ACCG

API REST desenvolvida com Django REST Framework para gerenciar usuários, associados, planos de contas, cobranças, pagamentos e avisos de vencimento.

## Funcionalidades

### Usuários

* Modelo customizado baseado em `AbstractUser`.
* Autenticação por JWT.
* Autenticação por sessão para a Browsable API.
* CRUD de usuários restrito a administradores.

### Associados

* Cadastro, listagem, atualização e exclusão de associados.
* Validação completa de CNPJ.
* Upload de contrato e ficha cadastral.
* Definição automática da data de vencimento.
* Histórico cadastral e financeiro consolidado.
* Avisos de vencimento por e-mail.

### Plano de contas

* Cadastro de contas de receita e despesa.
* Pesquisa, ordenação e filtros.
* Exclusão lógica por meio do campo `ativo`.

### Cobranças

* Cobranças vinculadas ao associado e ao plano de contas.
* Validação de valor e data de vencimento.
* Código local de gateway para testes.
* Filtros por status, associado, plano de contas e vencimento.
* Webhook protegido por token.
* Processamento idempotente de pagamentos.

> A integração com um gateway de pagamento real ainda não está implementada. Atualmente, a API gera um código local iniciado por `LOCAL-` para permitir testes do fluxo de cobrança e do webhook.

## Tecnologias

* Python 3.10, 3.11 ou 3.12
* Django 4.2.7
* Django REST Framework 3.14
* Simple JWT
* django-filter
* drf-spectacular
* django-cors-headers
* python-decouple
* SQLite para desenvolvimento

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/kaymmiNunes/api-accg.git
cd api-accg
```

### 2. Criar o ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo de variáveis de ambiente

No Windows:

```bash
copy .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure, no mínimo:

```env
DEBUG=True
SECRET_KEY=uma-chave-secreta-segura
ALLOWED_HOSTS=127.0.0.1,localhost
WEBHOOK_TOKEN=um-token-seguro
```

### 5. Executar as migrações

```bash
python manage.py migrate
```

### 6. Criar um superusuário

```bash
python manage.py createsuperuser
```

### 7. Verificar a configuração

```bash
python manage.py check
```

### 8. Executar o servidor

```bash
python manage.py runserver
```

O projeto ficará disponível em:

```text
http://127.0.0.1:8000/
```

## Autenticação JWT

### Obter os tokens

Envie uma requisição:

```http
POST /api/token/
Content-Type: application/json
```

Corpo da requisição:

```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

Exemplo de resposta:

```json
{
  "refresh": "token-de-renovacao",
  "access": "token-de-acesso"
}
```

### Utilizar o token de acesso

Inclua o token no cabeçalho das requisições protegidas:

```http
Authorization: Bearer token-de-acesso
```

### Renovar o token

```http
POST /api/token/refresh/
Content-Type: application/json
```

Corpo da requisição:

```json
{
  "refresh": "token-de-renovacao"
}
```

## Documentação da API

### Swagger

```text
http://127.0.0.1:8000/api/docs/
```

### Schema OpenAPI

```text
http://127.0.0.1:8000/api/schema/
```

## Principais endpoints

| Método         | Endpoint                          | Descrição                          |
| -------------- | --------------------------------- | ---------------------------------- |
| `POST`         | `/api/token/`                     | Obtém os tokens JWT                |
| `POST`         | `/api/token/refresh/`             | Renova o token de acesso           |
| `GET` e `POST` | `/api/users/`                     | Gerencia usuários                  |
| `GET` e `POST` | `/api/associados/`                | Gerencia associados                |
| `GET`          | `/api/associados/{id}/historico/` | Retorna o histórico do associado   |
| `GET` e `POST` | `/api/planos-contas/`             | Gerencia o plano de contas         |
| `GET` e `POST` | `/api/cobrancas/`                 | Gerencia cobranças                 |
| `POST`         | `/api/webhook/`                   | Processa notificações de pagamento |

## Cadastro de associado

Exemplo de requisição:

```http
POST /api/associados/
Authorization: Bearer token-de-acesso
Content-Type: application/json
```

Corpo:

```json
{
  "razao_social": "Empresa Exemplo Ltda",
  "nome_fantasia": "Empresa Exemplo",
  "cnpj": "11.222.333/0001-81",
  "email": "contato@empresa.com",
  "telefone": "85999999999",
  "endereco": "Rua Exemplo, 100"
}
```

O CNPJ pode ser enviado com ou sem pontuação. A API armazena somente os 14 dígitos.

## Cadastro de plano de contas

Exemplo de requisição:

```http
POST /api/planos-contas/
Authorization: Bearer token-de-acesso
Content-Type: application/json
```

Corpo:

```json
{
  "codigo": "1.1",
  "descricao": "Mensalidades de associados",
  "tipo": "RECEITA",
  "categoria": "Mensalidades",
  "observacoes": "Receitas provenientes das mensalidades"
}
```

Os tipos aceitos são:

* `RECEITA`
* `DESPESA`

## Criação de cobrança

Exemplo de requisição:

```http
POST /api/cobrancas/
Authorization: Bearer token-de-acesso
Content-Type: application/json
```

Corpo:

```json
{
  "associado": 1,
  "plano_conta": 1,
  "valor": "150.00",
  "descricao": "Mensalidade do associado",
  "data_vencimento": "2026-08-15"
}
```

A API gera automaticamente:

* Status inicial `PENDENTE`.
* Código local de gateway iniciado por `LOCAL-`.
* Data de criação.
* Data de atualização.

Exemplo de resposta:

```json
{
  "id": 1,
  "associado": 1,
  "associado_nome": "Empresa Exemplo Ltda",
  "plano_conta": 1,
  "plano_conta_descricao": "Mensalidades de associados",
  "valor": "150.00",
  "descricao": "Mensalidade do associado",
  "status": "PENDENTE",
  "data_vencimento": "2026-08-15",
  "codigo_gateway": "LOCAL-CODIGO-GERADO",
  "link_pagamento": null,
  "data_criacao": "2026-07-19T10:00:00-03:00",
  "data_atualizacao": "2026-07-19T10:00:00-03:00"
}
```

## Webhook de pagamento

O webhook é público, mas exige um token no cabeçalho `X-Webhook-Token`.

Exemplo de requisição:

```http
POST /api/webhook/
Content-Type: application/json
X-Webhook-Token: valor-configurado-no-env
```

Corpo:

```json
{
  "codigo_gateway": "LOCAL-CODIGO-DA-COBRANCA",
  "status": "PAGA"
}
```

Exemplo de resposta:

```json
{
  "mensagem": "Evento processado com sucesso.",
  "cobranca_id": 1,
  "status": "PAGA"
}
```

O processamento é idempotente. Caso uma cobrança já esteja paga, o recebimento repetido do mesmo evento não gera uma nova alteração.

## Histórico do associado

Endpoint:

```http
GET /api/associados/{id}/historico/
Authorization: Bearer token-de-acesso
```

O histórico contém:

* Informações do associado.
* Total pendente.
* Total pago.
* Total cancelado.
* Último pagamento.
* Indicação de cobrança atrasada.
* Lista de cobranças.
* Eventos cadastrais e financeiros.

## Filtros e pesquisas

### Cobranças

Filtrar por status:

```text
/api/cobrancas/?status=PENDENTE
```

Filtrar por associado:

```text
/api/cobrancas/?associado=1
```

Filtrar por plano de contas:

```text
/api/cobrancas/?plano_conta=1
```

Pesquisar pela descrição, associado, CNPJ ou código do gateway:

```text
/api/cobrancas/?search=mensalidade
```

Ordenar pelo vencimento:

```text
/api/cobrancas/?ordering=data_vencimento
```

Ordenar do vencimento mais recente para o mais antigo:

```text
/api/cobrancas/?ordering=-data_vencimento
```

### Plano de contas

Filtrar por tipo:

```text
/api/planos-contas/?tipo=RECEITA
```

Filtrar por categoria:

```text
/api/planos-contas/?categoria=Mensalidades
```

Pesquisar por código, descrição ou categoria:

```text
/api/planos-contas/?search=receita
```

Ordenar pela descrição:

```text
/api/planos-contas/?ordering=descricao
```

### Associados

Pesquisar por razão social, nome fantasia, CNPJ ou e-mail:

```text
/api/associados/?search=empresa
```

Ordenar pelo vencimento:

```text
/api/associados/?ordering=data_vencimento
```

## Avisos de vencimento

O projeto possui um comando Django para verificar associados com contratos próximos do vencimento.

Executar com os prazos padrão de 30 e 7 dias:

```bash
python manage.py check_vencimentos
```

Definir prazos específicos:

```bash
python manage.py check_vencimentos --dias 30 15 7
```

Simular a execução sem enviar e-mails:

```bash
python manage.py check_vencimentos --dry-run
```

No Windows, também pode ser usado:

```text
executar_alertas.bat
```

## Configuração de e-mail

Durante o desenvolvimento, os e-mails podem ser exibidos no terminal:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Para envio real pelo Gmail:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-aplicativo
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

Use uma senha de aplicativo do Google. Nunca registre credenciais reais no Git.

## Testes automatizados

Executar todos os testes:

```bash
python manage.py test
```

Executar os testes de um módulo específico:

```bash
python manage.py test users
```

```bash
python manage.py test associados
```

```bash
python manage.py test financeiro
```

```bash
python manage.py test cobranca
```

## Estrutura principal

```text
api-accg/
├── api_accg/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── associados/
│   ├── management/
│   │   └── commands/
│   │       └── check_vencimentos.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   └── views.py
├── cobranca/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── webhooks.py
├── financeiro/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── .env.example
├── .gitignore
├── executar_alertas.bat
├── manage.py
├── requirements.txt
└── README.md
```

## Migração de cobranças existentes

O campo `associado` foi inicialmente criado como opcional no banco para evitar falhas caso já existam cobranças antigas.

Depois de relacionar todas as cobranças antigas aos seus respectivos associados, o campo pode ser alterado para obrigatório:

```python
associado = models.ForeignKey(
    Associado,
    on_delete=models.PROTECT,
    related_name="cobrancas",
)
```

Depois da alteração:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Segurança

Antes de publicar a API em produção:

* Defina `DEBUG=False`.
* Utilize uma `SECRET_KEY` exclusiva.
* Configure corretamente `ALLOWED_HOSTS`.
* Restrinja as origens permitidas pelo CORS.
* Utilize HTTPS.
* Não armazene senhas ou tokens no repositório.
* Use PostgreSQL ou outro banco adequado para produção.
* Configure armazenamento apropriado para uploads.
* Configure logs de aplicação.
* Use um servidor WSGI, como Gunicorn.
* Utilize um proxy reverso, como Nginx.
* Valide a assinatura oficial do gateway de pagamento.
* Execute os testes antes do deploy.

## Verificação antes da execução

Execute:

```bash
python manage.py check
```

Depois:

```bash
python manage.py migrate
```

Em seguida:

```bash
python manage.py test
```

Por fim:

```bash
python manage.py runserver
```

## Licença

Este projeto está licenciado sob a licença MIT.

## Equipe

Projeto acadêmico desenvolvido sob orientação do Prof. Jose George.

* Humberto Silva
* Kaymmi Nunes Barbosa
* Mateus Sebastian
* Samuel Lucas
