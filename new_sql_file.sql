-- ============================================
-- Banco de Dados para Loja de Roupas com Cascata de Deleção
-- ============================================

-- ============================================
-- 1. Remover Tabelas Existentes (Se Existirem)
-- ============================================
-- Ordem de remoção: da tabela mais dependente para a menos dependente

DROP TABLE IF EXISTS parcelas;
DROP TABLE IF EXISTS pedido_produto;
DROP TABLE IF EXISTS usuario_favorita_produto;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS produto_forma_pagamento;
DROP TABLE IF EXISTS forma_pagamento;
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS funcionario;
DROP TABLE IF EXISTS endereco;
DROP TABLE IF EXISTS pessoa;

-- ============================================
-- 2. Criar Tabelas com ON DELETE CASCADE
-- ============================================

-- ============================================
-- Tabela: pessoa
-- ============================================
CREATE TABLE pessoa (
    id_pessoa INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('cliente', 'funcionario', 'adm') NOT NULL,
    cpf VARCHAR(11),
    nome VARCHAR(50),
    sexo CHAR(1),
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(20) NOT NULL,	
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================
-- Tabela: endereco
-- ============================================
CREATE TABLE endereco (
    id_endereco INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT,
    numero_casa INT,
    rua VARCHAR(50),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    cep INT,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: funcionario
-- ============================================
CREATE TABLE funcionario (
    cod_func INT PRIMARY KEY,
    salario DECIMAL(10,2),
    FOREIGN KEY (cod_func) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: cliente
-- ============================================
CREATE TABLE cliente (
    cod_cliente INT PRIMARY KEY,
    FOREIGN KEY (cod_cliente) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: estoque
-- ============================================
CREATE TABLE estoque (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(60),
    sexo CHAR(1),
    categoria VARCHAR(60),
    tamanho VARCHAR(10),
    cor VARCHAR(30),
    quantidade INT,
    preco DECIMAL(10,2)	
) ENGINE=InnoDB;

-- ============================================
-- Tabela: forma_pagamento
-- ============================================
CREATE TABLE forma_pagamento (
    id_forma_pagamento INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    permite_parcelamento BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: pedido
-- ============================================
CREATE TABLE pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_func INT ,
    id_endereco INT NOT NULL,
    id_forma_pagamento INT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    numero_parcelas INT DEFAULT 1, -- 1 indica pagamento à vista
    FOREIGN KEY (id_cliente) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_func) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco) ON DELETE CASCADE,
    FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: usuario_favorita_produto
-- ============================================
CREATE TABLE usuario_favorita_produto (
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_cliente, id_produto),
    FOREIGN KEY (id_cliente) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: pedido_produto
-- ============================================
CREATE TABLE pedido_produto (
    id_pedido INT,
    id_produto INT,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    PRIMARY KEY (id_pedido, id_produto),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

create table carrinho_compras(
id_pessoa INT,
id_produto INT,
quantidade INT,
PRIMARY KEY (id_pessoa, id_produto),
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: parcelas
-- ============================================
CREATE TABLE parcelas (
    id_parcela INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    numero_parcela INT NOT NULL,
    data_vencimento DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status ENUM('Pendente', 'Pago', 'Atrasado') DEFAULT 'Pendente',
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Tabela: produto_forma_pagamento
-- ============================================
CREATE TABLE produto_forma_pagamento (
    id_produto INT NOT NULL,
    id_forma_pagamento INT NOT NULL,
    max_parcelas INT DEFAULT NULL,
    PRIMARY KEY (id_produto, id_forma_pagamento),
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE,
    FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- 3. Inserir Dados de Teste
-- ============================================

-- ============================================
-- Inserir Dados na Tabela: pessoa
-- ============================================
INSERT INTO pessoa (tipo, nome, email, senha) values ('adm','Joao Pedro', 'a', 'a');
INSERT INTO pessoa (tipo, nome, email, senha) values ('funcionario','Joao Pedro', 'f', 'f');
INSERT INTO pessoa (tipo, nome, email, senha) values ('cliente','Joao Pedro', 'c', 'c');
INSERT INTO pessoa (tipo, cpf, nome, sexo, data_nascimento, telefone, email, senha)
VALUES
('cliente', '12345678901', 'João Silva', 'M', '1990-05-15', '11999999999', 'joao.silva@example.com', 'senha123'),
('funcionario', '23456789012', 'Maria Oliveira', 'F', '1985-08-22', '11888888888', 'maria.oliveira@example.com', 'senha456'),
('adm', '34567890123', 'Carlos Souza', 'M', '1975-12-05', '11777777777', 'carlos.souza@example.com', 'senha789'),
('cliente', '45678901234', 'Ana Pereira', 'F', '1995-03-30', '11666666666', 'ana.pereira@example.com', 'senha321');

-- ============================================
-- Inserir Dados na Tabela: endereco
-- ============================================
INSERT INTO endereco (id_pessoa, numero_casa, rua, bairro, cidade, estado, cep)
VALUES
(1, 100, 'Rua A', 'Bairro A', 'São Paulo', 'SP', 12345678),
(2, 200, 'Rua B', 'Bairro B', 'Rio de Janeiro', 'RJ', 23456789),
(3, 300, 'Rua C', 'Bairro C', 'Belo Horizonte', 'MG', 34567890),
(4, 400, 'Rua D', 'Bairro D', 'Curitiba', 'PR', 45678901);

-- ============================================
-- Inserir Dados na Tabela: funcionario
-- ============================================
INSERT INTO funcionario (cod_func, salario)
VALUES
(2, 3000.00),
(3, 5000.00); -- Apenas id_pessoa = 2 e 3 são funcionários e administradores

-- ============================================
-- Inserir Dados na Tabela: cliente
-- ============================================
INSERT INTO cliente (cod_cliente)
VALUES
(1),
(4); -- Apenas id_pessoa = 1 e 4 são clientes

-- ============================================
-- Inserir Dados na Tabela: estoque
-- ============================================
INSERT INTO estoque (nome, sexo, categoria, tamanho, cor, quantidade, preco)
VALUES
('Camiseta', 'U', 'Vestuário', 'M', 'Azul', 50, 49.90),
('Calça Jeans', 'U', 'Vestuário', 'G', 'Preta', 30, 89.90),
('Vestido', 'F', 'Vestuário', 'P', 'Vermelho', 20, 129.90),
('Tênis', 'U', 'Calçados', '42', 'Branco', 15, 199.90);

-- ============================================
-- Inserir Dados na Tabela: forma_pagamento
-- ============================================
INSERT INTO forma_pagamento (nome, permite_parcelamento)
VALUES
('Dinheiro', FALSE),
('Pix', FALSE),
('Débito', FALSE),
('Cartão de Crédito', TRUE),
('Cartão de Débito', FALSE);

-- ============================================
-- Inserir Dados na Tabela: produto_forma_pagamento
-- ============================================
-- Associar todas as formas de pagamento a todos os produtos
-- Para formas que permitem parcelamento, definir max_parcelas como 12; caso contrário, NULL

INSERT INTO produto_forma_pagamento (id_produto, id_forma_pagamento, max_parcelas)
SELECT 
    e.id_produto,
    fp.id_forma_pagamento,
    CASE 
        WHEN fp.permite_parcelamento THEN 12
        ELSE NULL
    END AS max_parcelas
FROM 
    estoque e
CROSS JOIN 
    forma_pagamento fp;

-- ============================================
-- Inserir Dados na Tabela: pedido
-- ============================================
INSERT INTO pedido (id_cliente, id_func, id_endereco, id_forma_pagamento, total, numero_parcelas)
VALUES
(1, 2, 1, 4, 149.80, 3), -- João Silva realiza um pedido com Cartão de Crédito em 3 parcelas
(4, 2, 4, 1, 89.90, 1);  -- Ana Pereira realiza um pedido com Dinheiro à vista

select * from pedido;


INSERT INTO pedido (id_cliente, id_endereco, id_forma_pagamento, total, numero_parcelas)
VALUES
(1, 1, 4, 149.80, 3); -- João Silva realiza um pedido com Cartão de Crédito em 3 parcelas Sem Baixa


-- ============================================
-- Inserir Dados na Tabela: pedido_produto
-- ============================================
INSERT INTO pedido_produto (id_pedido, id_produto, quantidade, preco_unitario)
VALUES
(1, 1, 2, 49.90), -- Pedido 1: 2 Camisetas
(1, 2, 1, 89.90), -- Pedido 1: 1 Calça Jeans
(2, 2, 1, 89.90); -- Pedido 2: 1 Calça Jeans

-- ============================================
-- Inserir Dados na Tabela: parcelas
-- ============================================
INSERT INTO parcelas (id_pedido, numero_parcela, data_vencimento, valor, status)
VALUES
(1, 1, DATE_ADD(CURDATE(), INTERVAL 1 MONTH), 49.93, 'Pago'),
(1, 2, DATE_ADD(CURDATE(), INTERVAL 2 MONTH), 49.93, 'Pendente'),
(1, 3, DATE_ADD(CURDATE(), INTERVAL 3 MONTH), 49.94, 'Pendente');

-- ============================================
-- Inserir Dados na Tabela: usuario_favorita_produto
-- ============================================
INSERT INTO usuario_favorita_produto (id_cliente, id_produto)
VALUES
(1, 1), -- João Silva gosta de Camisetas
(1, 3), -- João Silva gosta de Vestidos
(4, 2), -- Ana Pereira gosta de Calças Jeans
(4, 4); -- Ana Pereira gosta de Tênis

-- ============================================
-- 4. Verificar as Inserções
-- ============================================

-- Verificar Tabela: pessoa
SELECT * FROM pessoa;

-- Verificar Tabela: endereco
SELECT * FROM endereco;

-- Verificar Tabela: funcionario
SELECT * FROM funcionario;

-- Verificar Tabela: cliente
SELECT * FROM cliente;

-- Verificar Tabela: estoque
SELECT * FROM estoque;

-- Verificar Tabela: forma_pagamento
SELECT * FROM forma_pagamento;

-- Verificar Tabela: produto_forma_pagamento
SELECT * FROM produto_forma_pagamento;	

-- Verificar Tabela: pedido
SELECT * FROM pedido;

-- Verificar Tabela: pedido_produto
SELECT * FROM pedido_produto;

-- Verificar Tabela: parcelas
SELECT * FROM parcelas;

-- Verificar Tabela: usuario_favorita_produto
SELECT * FROM usuario_favorita_produto;

-- ============================================
-- Fim do Script
-- ============================================
