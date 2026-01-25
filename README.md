# API de Gerenciamento ACCG

## 📌 Visão Geral

A **API ACCG** é um sistema backend robusto desenvolvido para gerenciar as operações da ACCG. O sistema centraliza o controle de usuários, associados e movimentações financeiras, oferecendo uma interface RESTful segura e documentada para integração com frontends e serviços externos.

### 🎯 Propósito e Problema Resolvido

O sistema resolve a necessidade de centralização e controle digital dos processos da associação, substituindo controles manuais ou descentralizados. Ele permite:
- Gestão unificada da base de associados com histórico completo.
- Controle financeiro através de plano de contas e emissão de cobranças.
- Automação de status de pagamentos via integração (Webhooks).

---

## 🚀 Principais Funcionalidades

### 1. Gerenciamento de Usuários (`users`)
- Autenticação e Autorização (JWT/Session).
- Cadastro de operadores do sistema com credenciais seguras.
- Modelo de usuário estendido do Django (`AbstractUser`).

### 2. Gestão de Associados (`associados`)
- **CRUD Completo**: Cadastro de Razão Social, CNPJ, Contatos, etc.
- **Gestão de Arquivos**: Upload e armazenamento de Contratos e Fichas Cadastrais.
- **Regras de Negócio**:
    - Definição automática de vencimento do associado (1 ano a partir do cadastro).
    - Status controlados: `ATIVO`, `INATIVO`, `SUSPENSO`.
- **Histórico Unificado**: Endpoint dedicado para consolidar dados cadastrais e financeiros do associado.

### 3. Módulo Financeiro (`financeiro`)
- **Plano de Contas**: Estrutura hierárquica para categorizar Receitas e Despesas.
- **Soft Delete**: Exclusão lógica de contas (campo `ativo=False`), preservando integridade histórica.

### 4. Cobranças e Pagamentos (`cobranca`)
- **Emissão**: Geração de cobranças vinculadas ao Plano de Contas.
- **Integração**: Campos preparados para `codigo_gateway` e `link_pagamento`.
- **Webhooks**: Endpoint público para receber callbacks de gateways de pagamento e baixar cobranças automaticamente.

---

## 🏗️ Arquitetura e Estrutura

O projeto segue o padrão **MVT (Model-View-Template)** do Django, adaptado para API REST com **Django REST Framework (DRF)**.

### Estrutura de Pastas

```
api-accg/
├── api_accg/          # Configurações globais (Settings, URLs, WSGI)
├── associados/        # App: Gestão de empresas associadas e documentos
│   ├── models.py      # Entidade Associado e regras de data
│   ├── services.py    # Lógica de negócios (Histórico consolidado)
│   └── views.py       # ViewSets e Actions
├── cobranca/          # App: Gestão financeira operacional
│   ├── models.py      # Entidade Cobranca
│   ├── webhooks.py    # Processamento de callbacks de pagamento
│   └── views.py       # ViewSets
├── financeiro/        # App: Estrutura contábil
│   ├── models.py      # Plano de Contas
│   └── views.py       # ViewSets com Soft Delete
├── users/             # App: Controle de acesso
└── manage.py          # CLI do Django
```

### Tecnologias Utilizadas

- **Linguagem**: Python 3.13+
- **Framework Web**: Django 4.2.7
- **API Toolkit**: Django REST Framework (DRF) 3.14
- **Banco de Dados**: SQLite (Desenvolvimento) / PostgreSQL (Recomendado Prod.)
- **Documentação**: drf-spectacular (Swagger/OpenAPI 3)
- **Segurança**: django-cors-headers

## 🗄️ Banco de Dados

O projeto está configurado inicialmente para utilizar **SQLite**, ideal para desenvolvimento e testes rápidos pela sua simplicidade e zero configuração (arquivo `db.sqlite3`).

Para ambientes de **Produção**, é recomendada a migração para bancos de dados robustos como **PostgreSQL** ou **MySQL**. A abstração do ORM do Django permite essa transição apenas ajustando as configurações em `settings.py`.

---

## ⚙️ Configuração e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git

### Passo a Passo (Local)

1. **Clone o repositório**
   ```bash
    git clone "URL DO REPOSITORIO"
    cd api-accg
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variáveis de Ambiente**
   O projeto utiliza `settings.py` padrão. Para produção, configure:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`

5. **Execute as migrações**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor**
   ```bash
   python manage.py runserver
   ```

O sistema estará acessível em: `http://127.0.0.1:8000/`

---

## 📚 Documentação da API

A documentação interativa (Swagger UI) é gerada automaticamente pelo `drf-spectacular`.

- **Swagger UI**: [`http://127.0.0.1:8000/api/docs/`](http://127.0.0.1:8000/api/docs/)
- **Download Schema (YAML/JSON)**: [`http://127.0.0.1:8000/api/schema/`](http://127.0.0.1:8000/api/schema/)

### Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| **POST** | `/api/users/` | Cadastro de usuários |
| **GET** | `/api/associados/` | Listagem de associados |
| **GET** | `/api/associados/{id}/historico/` | Histórico financeiro e cadastral consolidado |
| **POST** | `/api/cobrancas/` | Criar nova cobrança |
| **POST** | `/api/webhook/` | Receber notificação de pagamento (Webhook) |
| **GET** | `/api/planos-contas/` | Listar plano de contas (apenas ativos) |

---

## ✅ Boas Práticas e Padrões

- **Padrão de Código**: PEP-8.
- **API Design**:
    - Uso de `ViewSets` e `Routers` para padronização de URLs.
    - `Serializers` para validação e transformação de dados.
- **Tratamento de Erros**: Respostas HTTP semânticas (400, 401, 404, 500) padronizadas pelo DRF.
- **Segurança**:
    - `CORS` configurado para permitir origens específicas.
    - Autenticação via Session (Dev) e extensível para JWT.
    - Senhas hashadas via PBKDF2 (Padrão Django).

---

## 📈 Escalabilidade e Evolução

A arquitetura modular permite fácil expansão. Possibilidades futuras:

1. **Gateway de Pagamento Real**: Implementar a lógica no `cobranca/views.py` e `webhooks.py` para integrar com ASAAS, Stripe ou Pagar.me.
2. **Dockerização**: Criar `Dockerfile` e `docker-compose.yml` para orquestração de containers.
3. **Tasks Assíncronas**: Usar Celery para envio de emails de cobrança e processamento pesado.
4. **Testes Automatizados**: Aumentar cobertura de testes em `tests.py` de cada app.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT 

---

## 👨‍💻 Autores

Este projeto foi desenvolvido como parte das atividades acadêmicas do curso, sob orientação do **Prof. Jose George**.

**Equipe de Desenvolvimento:**
- Humberto Silva
- João Vitor
- Kaymmi Nunes Barbosa
- Mateus Sebastian
- Samuel Lucas

---

