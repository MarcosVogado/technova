# ⚡ TechNova — Sistema de Gestão Comercial (Entrega 3 — Sistema Completo)

O **TechNova** é um ecossistema de gestão comercial focado em eletrônicos, integrando uma **API REST protegida por JWT** com uma **interface web futurista (tema Neon/Dark)** que **consome essa mesma API**. Esta é a Entrega 3, com foco em integração interface ↔ API, regras de negócio, validação de campos e qualidade arquitetural.

---

## 🎨 Identidade Visual
- **Nome:** TechNova OS
- **Tema:** *Cyber/Neon* sobre fundo escuro
- **Paleta própria:** Ciano Neon `#00f2ff` · Rosa Neon (alertas) `#ff0055` · Fundo `#05080a` · Painéis `#0d121b`
- Efeitos de digitação nos títulos, painéis "glass" com brilho dinâmico e feedback de transação.

## 🛠️ Tecnologias
* **Core:** Python 3.12+ / Django 6.0.5
* **API:** Django REST Framework 3.17
* **Autenticação:** JWT via `djangorestframework-simplejwt` (Bearer Token)
* **Banco (dev):** SQLite (sem instalação extra) — pronto para trocar por SQL Server em produção
* **Frontend:** HTML5 + JavaScript (fetch) + Bootstrap 5 + Bootstrap Icons
* **CORS:** `django-cors-headers` (acesso à API por clientes externos)
* **Documentação:** `drf-spectacular` (OpenAPI 3 + Swagger UI + Redoc)
* **Qualidade:** Testes unitários e de integração (Django `TestCase` + DRF `APIClient`)

## 🚀 Funcionalidades
- [x] **Login JWT:** tela de autenticação que obtém e armazena o token; refresh automático.
- [x] **Dashboard:** KPIs (clientes, produtos, vendas, faturamento) e alertas de estoque — **carregados via API**.
- [x] **CRUD de Produtos:** criar, editar e excluir pela interface, com validação.
- [x] **CRUD de Clientes:** criar, editar e excluir, com validação de CPF e e-mail.
- [x] **PDV / Nova Venda:** carrinho com múltiplos itens, cálculo de total e baixa automática de estoque.
- [x] **Histórico de Vendas:** listagem e detalhamento de cada transação (itens, vendedor, total).
- [x] **API protegida:** todos os endpoints exigem token JWT válido.

## 📐 Arquitetura
O projeto isola a lógica de negócio em uma **camada de serviço** (`core/services.py`), separada das views e da API.

| Camada | Tecnologia | Papel |
| :--- | :--- | :--- |
| **Apresentação** | Templates + JS (`fetch`) | Telas que consomem a API REST com Bearer Token |
| **API** | DRF + Simple JWT | Endpoints protegidos por autenticação JWT |
| **Negócio** | `services.py` | Baixa de estoque atômica e validação de integridade |
| **Persistência** | SQLite (dev) | Armazenamento relacional |

**Fluxo de autenticação:** a interface faz login em `/api/auth/login`, guarda o token e o envia no header `Authorization: Bearer <token>` em todas as chamadas. O cliente JS (`core/static/core/js/api.js`) centraliza o token, o refresh automático no erro 401 e a guarda de rota.

## 🔌 Endpoints da API

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Obtém o par de tokens (access + refresh) |
| `POST` | `/api/auth/refresh` | Renova o token de acesso |
| `GET/POST` | `/api/clientes/` | Lista / cria clientes |
| `GET/PUT/DELETE` | `/api/clientes/{id}/` | Detalha / edita / exclui cliente |
| `GET/POST` | `/api/produtos/` | Lista / cria produtos |
| `GET/PUT/DELETE` | `/api/produtos/{id}/` | Detalha / edita / exclui produto |
| `GET/POST` | `/api/vendas/` | Lista / registra vendas (com itens) |
| `GET` | `/api/relatorios/vendas/` | Resumo consolidado de vendas |

**Regras de negócio validadas:** estoque insuficiente bloqueia a venda; cliente com vendas não pode ser excluído; CPF deve ter 11 dígitos; preço/estoque não podem ser negativos.

## 📖 Documentação interativa da API (Swagger / OpenAPI)
A API é documentada automaticamente via **drf-spectacular** (OpenAPI 3):

| Recurso | URL |
| :--- | :--- |
| **Swagger UI** | http://127.0.0.1:8000/api/docs/ |
| **Redoc** | http://127.0.0.1:8000/api/redoc/ |
| **Schema (YAML)** | http://127.0.0.1:8000/api/schema/ |

No **Swagger UI**, use o botão **Authorize** e informe `Bearer <access_token>` (obtido em `/api/auth/login`) para testar os endpoints protegidos diretamente pelo navegador.

## 🔒 Como testar a proteção JWT das rotas
1. **Sem token** → deve ser negado (HTTP 401):
   ```bash
   curl -i http://127.0.0.1:8000/api/produtos/
   ```
2. **Obter o token:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"SEU_USUARIO\",\"password\":\"SUA_SENHA\"}"
   ```
3. **Com token** → deve autorizar (HTTP 200):
   ```bash
   curl -i http://127.0.0.1:8000/api/produtos/ -H "Authorization: Bearer SEU_ACCESS_TOKEN"
   ```
A verificação também é automatizada na suíte de testes (classe `JWTAuthTests`).

## ⚙️ Como Rodar o Sistema

1. **Ambiente virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Banco de dados (SQLite — criado automaticamente):**
   ```powershell
   python manage.py migrate
   ```

4. **Usuário de acesso** (necessário para logar no sistema e na API):
   ```powershell
   python manage.py createsuperuser
   ```

5. **Executar:**
   ```powershell
   python manage.py runserver
   ```
   Acesse **http://127.0.0.1:8000/** → você será direcionado ao **login**. Use as credenciais do superusuário criado.

> O painel administrativo do Django continua disponível em **http://127.0.0.1:8000/admin/**.

## 🧪 Testes
```powershell
python manage.py test core
```
Cobrem: regras de negócio (estoque/vendas), CRUD via API, validações de campo e **proteção JWT** (acesso negado sem token, login que autentica, credenciais inválidas).

## 📁 Estrutura
```
TechNova/
├── core/
│   ├── models.py          # Cliente, Produto, Venda, ItemVenda
│   ├── serializers.py     # Serialização + validações de campo
│   ├── services.py        # Camada de negócio (VendaService)
│   ├── views.py           # ViewSets da API + views web (shells)
│   ├── exceptions.py      # Exceções de negócio + handler customizado
│   ├── urls.py            # Rotas web e da API
│   ├── tests.py           # Testes unitários e de integração
│   ├── templates/core/    # login, dashboard, produtos, clientes, venda, histórico
│   └── static/core/       # main.css (tema neon) + api.js (cliente JWT) + main.js
├── setup/
│   ├── settings.py        # DRF, JWT, CORS, banco
│   └── urls.py            # Admin + JWT + inclusão de core.urls
└── requirements.txt
```

---
**Entrega 3** · Universalpay — Dinâmica de Devs
