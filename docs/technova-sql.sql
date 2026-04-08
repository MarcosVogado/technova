-- ============================================================
-- TechNova - Sistema de Gestão Comercial para Loja de Eletrônicos
-- Script de Criação do Banco de Dados (SQL Server)
-- ============================================================

-- Criação do banco de dados
CREATE DATABASE TechNova;
GO

USE TechNova;
GO

-- ============================================================
-- TABELA: usuarios
-- Armazena os dados dos usuários do sistema (admin/funcionário)
-- ============================================================
CREATE TABLE usuarios (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    username        VARCHAR(50)   NOT NULL UNIQUE,
    senha           VARCHAR(255)  NOT NULL,  -- hash BCrypt
    email           VARCHAR(100)  NOT NULL UNIQUE,
    perfil          VARCHAR(20)   NOT NULL DEFAULT 'FUNCIONARIO'
                        CHECK (perfil IN ('ADMIN', 'FUNCIONARIO')),
    ativo           BIT           NOT NULL DEFAULT 1,
    criado_em       DATETIME2     NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================
-- TABELA: clientes
-- Armazena os dados dos clientes da loja
-- ============================================================
CREATE TABLE clientes (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    nome            VARCHAR(150)  NOT NULL,
    cpf             VARCHAR(14)   NOT NULL UNIQUE,  -- formato: 000.000.000-00
    email           VARCHAR(100)  NOT NULL UNIQUE,
    telefone        VARCHAR(20)   NULL,
    endereco        VARCHAR(MAX)  NULL,
    criado_em       DATETIME2     NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================
-- TABELA: produtos
-- Armazena os produtos da loja de eletrônicos
-- ============================================================
CREATE TABLE produtos (
    id                  INT IDENTITY(1,1) PRIMARY KEY,
    nome                VARCHAR(200)   NOT NULL,
    descricao           VARCHAR(MAX)   NULL,
    categoria           VARCHAR(50)    NULL,
    preco               DECIMAL(10, 2) NOT NULL CHECK (preco >= 0),
    quantidade_estoque  INT            NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    estoque_minimo      INT            NOT NULL DEFAULT 5,
    ativo               BIT            NOT NULL DEFAULT 1,
    criado_em           DATETIME2      NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================
-- TABELA: vendas
-- Registra as vendas realizadas
-- ============================================================
CREATE TABLE vendas (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    data            DATETIME2      NOT NULL DEFAULT GETDATE(),
    valor_total     DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    observacoes     VARCHAR(MAX)   NULL,
    cliente_id      INT            NOT NULL,
    usuario_id      INT            NOT NULL,

    CONSTRAINT fk_venda_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE NO ACTION,

    CONSTRAINT fk_venda_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE NO ACTION
);
GO

-- ============================================================
-- TABELA: itens_venda
-- Armazena os itens individuais de cada venda
-- ============================================================
CREATE TABLE itens_venda (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    quantidade      INT            NOT NULL CHECK (quantidade > 0),
    preco_unitario  DECIMAL(10, 2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal        DECIMAL(12, 2) NOT NULL,
    venda_id        INT            NOT NULL,
    produto_id      INT            NOT NULL,

    CONSTRAINT fk_item_venda
        FOREIGN KEY (venda_id) REFERENCES vendas(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_produto
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
        ON DELETE NO ACTION
);
GO

-- ============================================================
-- ÍNDICES para melhorar a performance de consultas frequentes
-- ============================================================
CREATE INDEX idx_clientes_cpf        ON clientes(cpf);
CREATE INDEX idx_clientes_email      ON clientes(email);
CREATE INDEX idx_produtos_categoria  ON produtos(categoria);
CREATE INDEX idx_produtos_ativo      ON produtos(ativo);
CREATE INDEX idx_vendas_data         ON vendas(data);
CREATE INDEX idx_vendas_cliente      ON vendas(cliente_id);
CREATE INDEX idx_vendas_usuario      ON vendas(usuario_id);
CREATE INDEX idx_itens_venda_venda   ON itens_venda(venda_id);
CREATE INDEX idx_itens_venda_produto ON itens_venda(produto_id);
GO

-- ============================================================
-- DADOS INICIAIS: Usuário administrador padrão
-- Senha: admin123 (hash BCrypt gerado pela aplicação)
-- ============================================================
INSERT INTO usuarios (username, senha, email, perfil)
VALUES (
    'admin',
    '$2b$12$LJ3m4ys4yBxSGk6Z5K4e8eF7R1X2V3W4Y5Z6A7B8C9D0E1F2G3H4I',
    'admin@technova.com',
    'ADMIN'
);
GO

-- ============================================================
-- DADOS INICIAIS: Produtos de exemplo
-- ============================================================
INSERT INTO produtos (nome, descricao, categoria, preco, quantidade_estoque, estoque_minimo) VALUES
    ('Notebook Dell Inspiron 15', 'Intel Core i5, 8GB RAM, 256GB SSD', 'Notebooks', 3499.90, 15, 3),
    ('Mouse Logitech MX Master 3S', 'Mouse sem fio ergonômico, USB-C', 'Periféricos', 499.90, 30, 5),
    ('Monitor Samsung 24" Full HD', 'IPS, 75Hz, HDMI/VGA', 'Monitores', 899.90, 10, 2),
    ('Teclado Mecânico Redragon Kumara', 'Switch Red, RGB, ABNT2', 'Periféricos', 249.90, 25, 5),
    ('SSD Kingston 480GB SATA', '2.5", leitura 500MB/s', 'Componentes', 199.90, 40, 10),
    ('Smartphone Samsung Galaxy A54', '128GB, 6GB RAM, Tela 6.4"', 'Smartphones', 1899.90, 20, 3);
GO
