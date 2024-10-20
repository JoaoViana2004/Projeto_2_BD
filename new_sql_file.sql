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
    is_flamengo BOOLEAN,
    is_onepiece BOOLEAN,
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

CREATE TABLE log_acoes (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    tabela VARCHAR(50),
    operacao VARCHAR(10),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalhes TEXT
);

-- ================ VIEW ================
CREATE VIEW relatorio_vendas AS
SELECT pedido.id_pedido, pe.nome AS nome_cliente, f.nome AS nome_funcionario, pa.nome AS nome_forma_pagamento, pedido.data_cadastro AS data_pedido, pedido.total AS valor_total FROM pedido LEFT JOIN pessoa AS pe ON pedido.id_cliente = pe.id_pessoa LEFT JOIN pessoa AS f ON pedido.id_func = f.id_pessoa LEFT JOIN forma_pagamento AS pa ON pedido.id_forma_pagamento = pa.id_forma_pagamento  ORDER BY pedido.data_cadastro;

CREATE VIEW relatorio_usuarios AS
SELECT pessoa.id_pessoa AS id_cliente, pessoa.nome AS nome_cliente, COUNT(pedido.id_pedido) AS quantidade_compras, IFNULL(SUM(pedido.total), 0) AS total_gasto FROM pessoa LEFT JOIN pedido ON pessoa.id_pessoa = pedido.id_cliente WHERE pessoa.tipo = 'cliente' GROUP BY pessoa.id_pessoa, pessoa.nome  ORDER BY quantidade_compras DESC;

CREATE VIEW relatorio_estoque AS
SELECT estoque.id_produto, estoque.nome AS nome_produto, estoque.quantidade AS quantidade_estoque, IFNULL(SUM(pp.quantidade), 0) AS quantidade_vendida FROM estoque LEFT JOIN pedido_produto AS pp ON estoque.id_produto = pp.id_produto  GROUP BY estoque.id_produto, estoque.nome, estoque.quantidade  ORDER BY estoque.nome;

CREATE VIEW relatorio_funcionarios AS
 SELECT f.id_pessoa AS id_funcionario, f.nome AS nome_funcionario, COUNT(pedido.id_pedido) AS total_pedidos, SUM(pedido.total) AS total_dinheiro FROM pedido LEFT JOIN pessoa AS f ON pedido.id_func = f.id_pessoa WHERE f.tipo = 'funcionario' GROUP BY f.id_pessoa, f.nome  ORDER BY total_pedidos DESC;
-- ================ STORED PROCEDURE ================
DELIMITER //

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

CREATE TRIGGER log_insert_produto
AFTER INSERT ON produto
FOR EACH ROW
BEGIN
    INSERT INTO log_acoes (tabela, operacao, detalhes)
    VALUES ('produto', 'INSERT', CONCAT('ID: ', NEW.id, ', Nome: ', NEW.nome, ', Preco: ', NEW.preco));
END //

CREATE TRIGGER log_update_produto
AFTER UPDATE ON produto
FOR EACH ROW
BEGIN
    INSERT INTO log_acoes (tabela, operacao, detalhes)
    VALUES ('produto', 'UPDATE', CONCAT('ID: ', NEW.id, ', Nome: ', NEW.nome, ', Preco: ', NEW.preco));
END //

CREATE TRIGGER log_delete_produto
AFTER DELETE ON produto
FOR EACH ROW
BEGIN
    INSERT INTO log_acoes (tabela, operacao, detalhes)
    VALUES ('produto', 'DELETE', CONCAT('ID: ', OLD.id, ', Nome: ', OLD.nome, ', Preco: ', OLD.preco));
END //