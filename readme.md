# ⚡ TechNova — Sistema de Gestão Comercial (Entrega Final - Etapa 2)

O **TechNova** é um ecossistema de gestão comercial focado em eletrônicos, integrando uma **API REST robusta** com uma **Interface Web Futurista (Neon/Dark Mode)**. Este projeto representa a conclusão da Entrega 2, focando em integridade de dados, regras de negócio complexas e experiência do usuário.

---

## 📺 Demonstração de Testes (Vídeo)
Para facilitar a avaliação, gravei um vídeo demonstrando o sistema em funcionamento, desde o cadastro de produtos até a baixa automática de estoque em uma venda:
👉 **[CLIQUE AQUI PARA ASSISTIR AO VÍDEO DE TESTES](https://youtu.be/Nuv3-V5PWFc)**

---

## 🛠️ Tecnologias de Ponta
* **Core:** Python 3.12 / Django 6.0.5
* **Engine de Dados:** Microsoft SQL Server (Transações Atômicas)
* **Segurança & API:** Django REST Framework + JWT (Simple JWT)
* **Frontend:** HTML5/JS (Efeito Neon/Cyber) + Bootstrap 5 + Bi-Icons
* **Qualidade:** Unidade de Testes Django (TestCase)

## 🚀 Funcionalidades Chave (Checklist de Entrega)
- [x] **Dashboard Operacional:** Visualização em tempo real de KPIs e alertas de estoque baixo.
- [x] **Conexão SQL Server:** Integração total via `mssql-django`.
- [x] **Gestão de Estoque:** Lógica de baixa automática e bloqueio de vendas caso o saldo seja insuficiente.
- [x] **Interface PDV:** Módulo de nova venda com seleção dinâmica de cliente e produto.
- [x] **Histórico de Vendas:** Registro completo de transações integrando Frontend e Banco de Dados.
- [x] **Segurança JWT:** Endpoints de API protegidos para autenticação de dispositivos externos.

## 📐 Arquitetura do Sistema
O projeto utiliza uma estrutura de **Camadas de Serviço (Service Layer)** no `core/services.py`, isolando a lógica de negócio das visualizações.

| Camada | Tecnologia | Papel Estratégico |
| :--- | :--- | :--- |
| **Apresentação** | Django Templates / JS | Interface UX de alta tecnologia com feedback em tempo real. |
| **API** | DRF (REST) | Endpoints blindados com autenticação Bearer Token. |
| **Negócio** | `services.py` | Lógica de baixa de estoque e validação de integridade. |
| **Persistência** | SQL Server | Armazenamento relacional robusto com suporte a concorrência. |

## ⚙️ Como Rodar o Sistema (Guia para o Professor)

1.  **Ambiente Virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Instalação de Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuração do Banco de Dados:**
    * Certifique-se que o SQL Server (SQLEXPRESS) está rodando.
    * O banco de dados deve se chamar `technova`.
    ```bash
    python manage.py migrate
    ```

4.  **Execução:**
    ```bash
    python manage.py runserver
    ```
    Acesse: `http://127.0.0.1:8000/`

## 🧪 Testes de Qualidade
Para validar as regras de negócio:
```bash
python manage.py test core

Os testes cobrem: CRUDs, Saldo de Estoque e Fluxo de Vendas.

Status da Entrega: ✅ Concluída | Desenvolvido por: João César Netto S. Castro