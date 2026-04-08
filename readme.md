# ⚡ TechNova — Sistema de Gestão Comercial para Loja de Eletrônicos

Sistema de Gestão Comercial desenvolvido como projeto acadêmico para a disciplina de Programação. Aplicado ao contexto de uma **loja de eletrônicos**, com controle de clientes, produtos, vendas, estoque e relatórios.

## 🛠️ Tecnologias

- **Backend**: Python 3.10+ / Django 5.x / Django REST Framework
- **Banco de Dados**: SQL Server 2019+
- **Driver BD**: mssql-django + pyodbc
- **Autenticação**: JWT (Simple JWT)
- **Frontend**: Django Templates + Bootstrap 5
- **Gráficos**: Chart.js
- **Testes**: pytest + Django TestCase

## 📐 Arquitetura

O sistema segue uma **Arquitetura em Camadas**:

| Camada         | Responsabilidade                            | Tecnologia          |
|----------------|---------------------------------------------|---------------------|
| Apresentação   | Interface web, consumo da API               | Django Templates    |
| API            | Endpoints REST, serialização                | DRF                 |
| Negócio        | Validações, cálculos, regras                | Services (Python)   |
| Persistência   | Mapeamento objeto-relacional, queries       | Django ORM          |

## 📂 Estrutura do Projeto

```
technova/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/                           # Documentação do projeto
│   ├── entrega1_modelagem.pdf
│   ├── diagrama_classes.png
│   ├── diagrama_banco.png
│   └── script_banco.sql
│
├── technova/                       # Configuração principal do Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                           # Aplicações Django
│   ├── usuarios/                   # Autenticação e perfis
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── clientes/                   # CRUD de clientes
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── produtos/                   # CRUD de produtos e estoque
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   └── vendas/                     # Vendas e relatórios
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── services.py
│       ├── urls.py
│       └── admin.py
│
├── templates/                      # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── clientes/
│   │   ├── lista.html
│   │   └── formulario.html
│   ├── produtos/
│   │   ├── lista.html
│   │   └── formulario.html
│   ├── vendas/
│   │   ├── lista.html
│   │   ├── detalhe.html
│   │   └── nova_venda.html
│   └── relatorios/
│       └── vendas.html
│
└── static/                         # Arquivos estáticos
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── img/
        └── logo.png
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- SQL Server 2019+ (ou SQL Server Express)
- ODBC Driver 17 ou 18 for SQL Server
- pip

### Passos

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/technova.git
cd technova

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar o banco de dados no SQL Server
# Execute o script docs/script_banco.sql no SSMS ou sqlcmd

# 5. Configurar a conexão em technova/settings.py
# Edite DATABASES com seu servidor, usuário e senha

# 6. Executar migrations
python manage.py migrate

# 7. Criar superusuário
python manage.py createsuperuser

# 8. Iniciar servidor
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 📋 Endpoints da API

| Método | Endpoint            | Descrição                   |
|--------|---------------------|-----------------------------|
| POST   | /api/auth/login     | Login (retorna JWT)         |
| GET    | /api/clientes       | Listar clientes             |
| POST   | /api/clientes       | Cadastrar cliente           |
| PUT    | /api/clientes/{id}  | Atualizar cliente           |
| DELETE | /api/clientes/{id}  | Excluir cliente             |
| GET    | /api/produtos       | Listar produtos             |
| POST   | /api/produtos       | Cadastrar produto           |
| PUT    | /api/produtos/{id}  | Atualizar produto           |
| DELETE | /api/produtos/{id}  | Excluir produto             |
| GET    | /api/vendas         | Listar vendas               |
| GET    | /api/vendas/{id}    | Detalhar venda              |
| POST   | /api/vendas         | Registrar venda             |
| GET    | /api/relatorios     | Relatório de vendas         |

## 👥 Equipe

- [Nome 1]
- [Nome 2]
- [Nome 3]

## 📄 Documentação

A documentação completa está disponível na pasta `/docs/`:
- Documento de modelagem e arquitetura (PDF)
- Diagrama de Classes
- Diagrama Lógico do Banco de Dados
- Script SQL de criação do banco

## 📅 Entregas

| Entrega | Data  | Foco                           | Status |
|---------|-------|--------------------------------|--------|
| 1       | 08/04 | Modelagem e Arquitetura        | ✅      |
| 2       | 13/05 | Backend e API                  | 🔲      |
| 3       | 24/06 | Sistema Completo               | 🔲      |

---

> Projeto acadêmico — TechNova © 2026
