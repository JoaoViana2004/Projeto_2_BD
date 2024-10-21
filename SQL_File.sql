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
DROP TABLE IF EXISTS carrinho_compras;
DROP TABLE IF EXISTS forma_pagamento;
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS funcionario;
DROP TABLE IF EXISTS endereco;
DROP TABLE IF EXISTS pessoa;

-- ============================================
-- 2. Criar Tabelas com ON DELETE CASCADE
-- ============================================
-- Tabela: pessoa
CREATE TABLE pessoa (
    id_pessoa INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('cliente', 'funcionario', 'adm') NOT NULL,
    cpf VARCHAR(11),
    nome VARCHAR(50),
    data_nascimento DATE,
    is_flamengo BOOLEAN,
    is_onepiece BOOLEAN,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(20) NOT NULL,	
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabela: endereco
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

-- Tabela: funcionario
CREATE TABLE funcionario (
    cod_func INT PRIMARY KEY,
    salario DECIMAL(10,2),
    FOREIGN KEY (cod_func) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: cliente
CREATE TABLE cliente (
    cod_cliente INT PRIMARY KEY,
    FOREIGN KEY (cod_cliente) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: estoque
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

-- Tabela: forma_pagamento
CREATE TABLE forma_pagamento (
    id_forma_pagamento INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    permite_parcelamento BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;

-- Tabela: pedido
CREATE TABLE pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_func INT,
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

-- Tabela: usuario_favorita_produto
CREATE TABLE usuario_favorita_produto (
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_cliente, id_produto),
    FOREIGN KEY (id_cliente) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: pedido_produto
CREATE TABLE pedido_produto (
    id_pedido INT,
    id_produto INT,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    PRIMARY KEY (id_pedido, id_produto),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: carrinho_compras
CREATE TABLE carrinho_compras(
    id_pessoa INT,
    id_produto INT,
    quantidade INT,
    PRIMARY KEY (id_pessoa, id_produto),
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: parcelas
CREATE TABLE parcelas (
    id_parcela INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    numero_parcela INT NOT NULL,
    data_vencimento DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status ENUM('Pendente', 'Pago', 'Atrasado') DEFAULT 'Pendente',
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: produto_forma_pagamento
CREATE TABLE produto_forma_pagamento (
    id_produto INT NOT NULL,
    id_forma_pagamento INT NOT NULL,
    max_parcelas INT DEFAULT NULL,
    PRIMARY KEY (id_produto, id_forma_pagamento),
    FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE,
    FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela: log_acoes
DROP TABLE IF EXISTS log_acoes;
CREATE TABLE log_acoes (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    tabela VARCHAR(50),
    operacao VARCHAR(10),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalhes TEXT
) ENGINE=InnoDB;

-- ================ VIEW ================
DROP VIEW IF EXISTS relatorio_vendas;
CREATE VIEW relatorio_vendas AS
SELECT pedido.id_pedido, pe.nome AS nome_cliente, f.nome AS nome_funcionario, pa.nome AS nome_forma_pagamento, pedido.data_cadastro AS data_pedido, pedido.total AS valor_total 
FROM pedido 
LEFT JOIN pessoa AS pe ON pedido.id_cliente = pe.id_pessoa 
LEFT JOIN pessoa AS f ON pedido.id_func = f.id_pessoa 
LEFT JOIN forma_pagamento AS pa ON pedido.id_forma_pagamento = pa.id_forma_pagamento  
ORDER BY pedido.data_cadastro;

DROP VIEW IF EXISTS relatorio_usuarios;
CREATE VIEW relatorio_usuarios AS
SELECT pessoa.id_pessoa AS id_cliente, pessoa.nome AS nome_cliente, COUNT(pedido.id_pedido) AS quantidade_compras, IFNULL(SUM(pedido.total), 0) AS total_gasto 
FROM pessoa 
LEFT JOIN pedido ON pessoa.id_pessoa = pedido.id_cliente 
WHERE pessoa.tipo = 'cliente' 
GROUP BY pessoa.id_pessoa, pessoa.nome  
ORDER BY quantidade_compras DESC;

DROP VIEW IF EXISTS relatorio_estoque;
CREATE VIEW relatorio_estoque AS
SELECT estoque.id_produto, estoque.nome AS nome_produto, estoque.quantidade AS quantidade_estoque, IFNULL(SUM(pp.quantidade), 0) AS quantidade_vendida 
FROM estoque 
LEFT JOIN pedido_produto AS pp ON estoque.id_produto = pp.id_produto  
GROUP BY estoque.id_produto, estoque.nome, estoque.quantidade  
ORDER BY estoque.nome;

DROP VIEW IF EXISTS relatorio_funcionarios;
CREATE VIEW relatorio_funcionarios AS
SELECT f.id_pessoa AS id_funcionario, f.nome AS nome_funcionario, COUNT(pedido.id_pedido) AS total_pedidos, SUM(pedido.total) AS total_dinheiro 
FROM pedido 
LEFT JOIN pessoa AS f ON pedido.id_func = f.id_pessoa 
WHERE f.tipo = 'funcionario' 
GROUP BY f.id_pessoa, f.nome  
ORDER BY total_pedidos DESC;

-- ================ STORED PROCEDURE ================
DELIMITER //
DROP PROCEDURE IF EXISTS relatorio_funcionarios;
CREATE PROCEDURE relatorio_funcionarios(IN data_inicio DATE, IN data_fim DATE)
BEGIN
    SELECT 
        f.cod_func AS ID_funcionario,
        p.nome AS Nome_Funcionario,
        COUNT(pedido.id_pedido) AS Total_Pedidos_Efetivados,
        SUM(pedido.total) AS Total_Em_Dinheiro
    FROM 
        funcionario f
    JOIN 
        pessoa p ON f.cod_func = p.id_pessoa
    JOIN 
        pedido ON f.cod_func = pedido.id_func
    WHERE 
        pedido.data_cadastro BETWEEN data_inicio AND data_fim
    GROUP BY 
        f.cod_func, p.nome
    ORDER BY 
        Total_Pedidos_Efetivados DESC;
END //

DELIMITER ;

-- ============== Trigger ====================
DROP TRIGGER IF EXISTS `test_screma`.`estoque_BEFORE_INSERT`;

DELIMITER $$
USE `test_screma`$$
CREATE DEFINER = CURRENT_USER TRIGGER `test_screma`.`estoque_BEFORE_INSERT` BEFORE INSERT ON `estoque` FOR EACH ROW
BEGIN
INSERT INTO log_acoes (tabela, operacao, detalhes)
    VALUES ('produto', 'INSERT', CONCAT('ID: ', NEW.id_produto, ', Nome: ', NEW.nome, ', Preço: ', NEW.preco, ', Quantidade: ', NEW.quantidade));
END;
$$

DELIMITER ;

-- ============== Dados de Exemplo ====================
-- Inserir dados na tabela pessoa
INSERT INTO pessoa (tipo, cpf, nome, data_nascimento, is_flamengo, is_onepiece, telefone, email, senha)
VALUES
('cliente', '12345678901', 'João Silva', '1990-01-15', TRUE, FALSE, '1234567890', 'joao.silva@example.com', 'senha123'),
('cliente', '23456789012', 'Maria Santos', '1985-03-22', FALSE, TRUE, '0987654321', 'maria.santos@example.com', 'senha456'),
('cliente', '34567890123', 'Pedro Alves', '1978-07-11', FALSE, FALSE, '1112223333', 'pedro.alves@example.com', 'senha789'),
('cliente', '45678901234', 'Ana Lima', '1988-07-19', TRUE, TRUE, '4445556666', 'ana.lima@example.com', 'senha101'),
('cliente', '56789012345', 'Lucas Pereira', '1992-09-10', TRUE, FALSE, '7778889999', 'lucas.pereira@example.com', 'senha111'),
('cliente', '67890123456', 'Beatriz Rocha', '1983-12-01', FALSE, TRUE, '2223334444', 'beatriz.rocha@example.com', 'senha222'),
('cliente', '78901234567', 'Carla Costa', '1995-04-18', TRUE, FALSE, '5556667777', 'carla.costa@example.com', 'senha333'),
('cliente', '89012345678', 'Fabio Nunes', '1991-11-29', FALSE, FALSE, '8889990000', 'fabio.nunes@example.com', 'senha444'),
('cliente', '90123456789', 'Juliana Araújo', '1986-06-23', TRUE, TRUE, '3334445555', 'juliana.araujo@example.com', 'senha555'),
('cliente', '01234567890', 'Rafael Almeida', '1993-08-14', FALSE, FALSE, '6667778888', 'rafael.almeida@example.com', 'senha666'),
('funcionario', '11234567890', 'Carlos Souza', '1975-05-30', FALSE, FALSE, '1233211234', 'carlos.souza@example.com', 'senha789'),
('funcionario', '22345678901', 'Fernanda Lima', '1982-02-17', TRUE, TRUE, '2344322345', 'fernanda.lima@example.com', 'senha987'),
('funcionario', '33456789012', 'José Silva', '1990-09-23', FALSE, TRUE, '3455433456', 'jose.silva@example.com', 'senha654'),
('adm', '44567890123', 'Admin User', '1992-09-10', TRUE, FALSE, '7778889999', 'admin@example.com', 'adminpass');

-- Inserir dados na tabela endereco
INSERT INTO endereco (id_pessoa, numero_casa, rua, bairro, cidade, estado, cep)
VALUES
(1, 101, 'Rua A', 'Bairro X', 'Cidade Y', 'PB', 58000001),
(2, 202, 'Rua B', 'Bairro Y', 'Cidade Z', 'PB', 58000002),
(3, 303, 'Rua C', 'Bairro Z', 'Cidade X', 'PB', 58000003),
(4, 404, 'Rua D', 'Bairro W', 'Cidade W', 'PB', 58000004),
(5, 505, 'Rua E', 'Bairro V', 'Cidade V', 'PB', 58000005),
(6, 606, 'Rua F', 'Bairro U', 'Cidade U', 'PB', 58000006),
(7, 707, 'Rua G', 'Bairro T', 'Cidade T', 'PB', 58000007),
(8, 808, 'Rua H', 'Bairro S', 'Cidade S', 'PB', 58000008),
(9, 909, 'Rua I', 'Bairro R', 'Cidade R', 'PB', 58000009),
(10, 1010, 'Rua J', 'Bairro Q', 'Cidade Q', 'PB', 58000010),
(11, 1111, 'Rua K', 'Bairro P', 'Cidade P', 'PB', 58000011),
(12, 1212, 'Rua L', 'Bairro O', 'Cidade O', 'PB', 58000012),
(13, 1313, 'Rua M', 'Bairro N', 'Cidade N', 'PB', 58000013);

-- Inserir dados na tabela funcionario
INSERT INTO funcionario (cod_func, salario)
VALUES
(11, 3000.00),
(12, 3500.00),
(13, 4000.00);

-- Inserir dados na tabela cliente
INSERT INTO cliente (cod_cliente)
VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);

-- Inserir dados na tabela estoque
INSERT INTO estoque (nome, sexo, categoria, tamanho, cor, quantidade, preco)
VALUES
('Camiseta Azul', 'M', 'Camiseta', 'M', 'Azul', 50, 29.90),
('Calça Jeans', 'F', 'Calça', '38', 'Azul', 30, 79.90),
('Vestido Vermelho', 'F', 'Vestido', 'M', 'Vermelho', 20, 99.90),
('Camisa Social Branca', 'M', 'Camisa', 'G', 'Branca', 40, 49.90),
('Saia Preta', 'F', 'Saia', 'P', 'Preto', 25, 39.90),
('Bermuda Cinza', 'M', 'Bermuda', 'G', 'Cinza', 35, 44.90),
('Jaqueta Jeans', 'M', 'Jaqueta', 'M', 'Azul', 15, 89.90),
('Blusa Verde', 'F', 'Blusa', 'M', 'Verde', 45, 29.90);

-- Inserir dados na tabela forma_pagamento
INSERT INTO forma_pagamento (nome, permite_parcelamento)
VALUES
('Cartão de Crédito', TRUE),
('Boleto', FALSE),
('Pix', FALSE);

-- Inserir dados na tabela pedido
INSERT INTO pedido (id_cliente, id_func, id_endereco, id_forma_pagamento, total, numero_parcelas)
VALUES
(1, 11, 1, 1, 150.00, 3),
(2, 12, 2, 2, 80.00, 1),
(3, 11, 3, 3, 120.00, 1),
(4, 13, 4, 1, 90.00, 2),
(5, 12, 5, 2, 50.00, 1),
(6, 13, 6, 1, 200.00, 4),
(7, 11, 7, 3, 140.00, 1),
(8, 13, 8, 1, 160.00, 2);

-- Inserir dados na tabela usuario_favorita_produto
INSERT INTO usuario_favorita_produto (id_cliente, id_produto)
VALUES
(1, 1),
(1, 3),
(2, 2),
(2, 5),
(3, 4),
(4, 6),
(5, 7),
(6, 8);

-- Inserir dados na tabela pedido_produto
INSERT INTO pedido_produto (id_pedido, id_produto, quantidade, preco_unitario)
VALUES
(1, 1, 2, 29.90),
(1, 2, 1, 79.90),
(2, 3, 1, 99.90),
(3, 4, 1, 49.90),
(4, 5, 1, 39.90),
(4, 6, 2, 44.90),
(5, 7, 1, 89.90),
(6, 8, 4, 29.90),
(7, 1, 2, 29.90),
(7, 4, 1, 49.90),
(8, 2, 2, 79.90);

-- Inserir dados na tabela carrinho_compras
INSERT INTO carrinho_compras (id_pessoa, id_produto, quantidade)
VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 1),
(4, 5, 2),
(5, 7, 1),
(6, 8, 1),
(7, 4, 1),
(8, 6, 3),
(9, 5, 1),
(10, 2, 2);

-- Inserir dados na tabela parcela


INSERT INTO parcelas (id_pedido, numero_parcela, data_vencimento, valor, status)
VALUES
(1, 1, '2024-01-15', 50.00, 'Pendente'),
(1, 2, '2024-02-15', 50.00, 'Pendente'),
(1, 3, '2024-03-15', 50.00, 'Pendente'),
(4, 1, '2024-01-20', 45.00, 'Pendente'),
(4, 2, '2024-02-20', 45.00, 'Pendente'),
(6, 1, '2024-01-10', 50.00, 'Pendente'),
(6, 2, '2024-02-10', 50.00, 'Pendente'),
(6, 3, '2024-03-10', 50.00, 'Pendente'),
(6, 4, '2024-04-10', 50.00, 'Pendente'),
(8, 1, '2024-01-05', 80.00, 'Pendente'),
(8, 2, '2024-02-05', 80.00, 'Pendente');

COMMIT;
