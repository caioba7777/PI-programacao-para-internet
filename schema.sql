-- 1. CRIAÇÃO E SELEÇÃO DO BANCO DE DADOS
CREATE DATABASE IF NOT EXISTS tech_store
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tech_store;

-- Remove as tabelas na ordem inversa das chaves estrangeiras para evitar erros de trava (Lock)
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS perfis;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS categorias;

-- 2. TABELA: CATEGORIAS
CREATE TABLE categorias (
    id_categoria BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    status VARCHAR(20) DEFAULT 'Ativa',
    setor VARCHAR(50),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. TABELA: PRODUTOS
CREATE TABLE produtos (
    id_produto BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    categoria_id BIGINT UNSIGNED NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_produto_categoria
        FOREIGN KEY (categoria_id) REFERENCES categorias (id_categoria)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 4. TABELA: PERFIS (Criada antes de 'usuarios' para permitir a chave estrangeira)
CREATE TABLE perfis (
    id_perfil BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao VARCHAR(255),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. TABELA: USUÁRIOS
CREATE TABLE usuarios (
    id_usuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    perfil_id BIGINT UNSIGNED NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_perfil
        FOREIGN KEY (perfil_id) REFERENCES perfis (id_perfil)
        ON DELETE RESTRICT ON UPDATE CASCADE
);