# API ACCG

API REST desenvolvida com Django REST Framework para o projeto ACCG.

## 🚀 Tecnologias

- **Python 3.13**
- **Django 4.2.7** - Framework web Python
- **Django REST Framework 3.14.0** - Framework para construção de APIs REST
- **django-cors-headers 4.3.1** - Middleware para lidar com CORS
- **SQLite** - Banco de dados (desenvolvimento)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação e Configuração

### 1. Clone o repositório (se aplicável)

```bash
git clone <url-do-repositorio>
cd ACCG
```

### 2. Ative o ambiente virtual

**No macOS/Linux:**
```bash
source venv/bin/activate
```

**No Windows:**
```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

## ▶️ Como Executar o Projeto

### 1. Ative o ambiente virtual

```bash
source venv/bin/activate
```

### 2. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000/`

### 3. Acesse os endpoints

- **Admin Django**: `http://127.0.0.1:8000/admin/`
- **API REST Framework**: `http://127.0.0.1:8000/api-auth/`

## 📁 Estrutura do Projeto

```
ACCG/
├── api_accg/          # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py    # Configurações do projeto
│   ├── urls.py        # URLs principais
│   ├── wsgi.py
│   └── asgi.py
├── manage.py          # Script de gerenciamento do Django
├── requirements.txt   # Dependências do projeto
├── .gitignore        # Arquivos ignorados pelo Git
├── README.md         # Este arquivo
└── venv/             # Ambiente virtual Python
```

## 🗄️ Banco de Dados

O projeto está configurado para usar **SQLite** como banco de dados. O arquivo `db.sqlite3` será criado automaticamente após executar as migrações.

## 🔐 Configurações de Segurança

⚠️ **Importante**: Este projeto está configurado para desenvolvimento. Para produção:

1. Altere `DEBUG = False` em `settings.py`
2. Configure `ALLOWED_HOSTS` adequadamente
3. Use uma `SECRET_KEY` segura e única
4. Configure `CORS_ALLOW_ALL_ORIGINS = False` e defina `CORS_ALLOWED_ORIGINS` com as origens permitidas
5. Use um banco de dados de produção (PostgreSQL, MySQL, etc.)

## 📝 Comandos Úteis

### Criar uma nova aplicação Django
```bash
python manage.py startapp nome_da_app
```

### Criar migrações
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido para o projeto ACCG.

Prof. Jose George 

Alunos: 

1.
2.
3.
4.
5. Samuel Lucas 

