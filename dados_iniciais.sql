USE tech_store;

-- 1. Popula os Perfis primeiro (Garante os IDs de 1 a 5)
INSERT INTO perfis (nome) VALUES 
('Administrador'), ('Gerente'), ('Vendedor'), ('Atendente'), ('Operador');

-- 2. Popula os Usuários vinculados aos IDs dos Perfis acima
INSERT INTO usuarios (nome, email, senha, perfil_id) VALUES
('Caio Silva', 'caio@email.com', 'senha123', 1),
('Ana Souza', 'ana@email.com', 'senha123', 2),
('Lucas Mendes', 'lucas@email.com', 'senha123', 3),
('Bruna Lima', 'bruna@email.com', 'senha123', 4),
('Marcos Alves', 'marcos@email.com', 'senha123', 5);

-- 3. Popula as Categorias (Garante os IDs necessários para os produtos)
INSERT INTO categorias (nome, descricao, status, setor) VALUES
('Periféricos', 'Produtos de entrada e interação', 'Ativa', 'Tecnologia'),
('Monitores', 'Telas e monitores para uso geral', 'Ativa', 'Tecnologia'),
('Áudio', 'Fones, caixas de som e headsets', 'Ativa', 'Eletrônicos'),
('Informática', 'Equipamentos e acessórios de informática', 'Ativa', 'Tecnologia'),
('Escritório', 'Itens voltados para rotina administrativa', 'Ativa', 'Administrativo');

-- 4. Popula os Produtos vinculados às Categorias criadas
INSERT INTO produtos (nome, preco, estoque, categoria_id) VALUES
('Mouse Gamer', 150.00, 50, 1),
('Teclado Mecânico', 299.90, 30, 1),
('Monitor 24 Polegadas', 899.00, 15, 2),
('Fone de Ouvido Bluetooth', 199.00, 40, 3),
('Cadeira de Escritório', 450.00, 10, 5);