⚡ TechNova — Sistema de Gestão Comercial (Entrega 2)
O TechNova é um ecossistema de gestão comercial focado em eletrônicos, integrando uma API REST robusta com uma Interface Web Futurista. Este projeto é o núcleo da Entrega 2, focando na integridade de dados e regras de negócio complexas.

🛠️ Tecnologias de Ponta
Core: Python 3.12 / Django 5.x

Engine de Dados: Microsoft SQL Server (Transações Atômicas)

Segurança & API: Django REST Framework + JWT (Simple JWT)

Frontend: HTML5/JS (Efeito Neon/Cyber) + Bootstrap 5

Qualidade: Unidade de Testes Django (TestCase)

📐 Arquitetura do Sistema
O projeto evoluiu para uma estrutura de Camadas de Serviço (Service Layer), isolando a lógica complexa:

Camada	Tecnologia	Papel Estratégico
Apresentação	Django Templates / JS	Interface com UX de alta tecnologia e feedback em tempo real.
API	DRF	Endpoints blindados com autenticação Bearer Token.
Negócio	services.py	Lógica de baixa de estoque e validação de integridade.
Exceções	exceptions.py	Tratamento customizado de erros (ex: Estoque Insuficiente).
Persistência	SQL Server	Armazenamento relacional com suporte a concorrência.
🚀 Funcionalidades Chave (Checklist Entrega 2)
[x] Conexão SQL Server: Integração total via mssql-django.

[x] Gestão de Estoque: Baixa automática e bloqueio de vendas acima do saldo disponível.

[x] Segurança JWT: Endpoints de login e refresh configurados conforme especificação.

[x] Relatórios Avançados: Endpoint dedicado para BI e resumo de faturamento mensal.

[x] Proteção de Dados: Bloqueio de exclusão de clientes com histórico de vendas (on_delete=models.PROTECT).

🧪 Testes de Qualidade
Para validar as regras de negócio e garantir que nenhum bug chegue à produção:

Bash
python manage.py test core
Os testes cobrem: CRUDs, Validação de CPF, Saldo de Estoque e Fluxo de Vendas.

⚙️ Instalação e Setup
Bash
# 1. Dependências
pip install -r requirements.txt

# 2. Banco de Dados
# Certifique-se que o SQL Server está rodando e o banco 'technova' está criado.
python manage.py migrate

# 3. Execução
python manage.py runserver
📋 Endpoints Estratégicos da API
Método	Endpoint	Objetivo
POST	/api/auth/login	Autenticação e geração de Token JWT.
POST	/api/vendas/	Registro de venda com transação atômica.
GET	/api/relatorios/vendas/	Dashboard de performance comercial.
Status da Entrega 2: ✅ Concluída com sucesso.

TechNova © 2026 — Desenvolvido por João César Netto S. Castro.