
PRAGMA journal_mode = WAL;

--- ============================================
--- USUARIO
--- ============================================
CREATE TABLE IF NOT EXISTS usuario (
    email      TEXT PRIMARY KEY,
    senha_hash TEXT NOT NULL,
    nome       TEXT NOT NULL,
    telefone   TEXT,
    cep        TEXT,
    ativo      INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

--- ============================================
--- AUTOR
--- ============================================
CREATE TABLE IF NOT EXISTS autor (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

--- ============================================
--- GENERO
--- ============================================
CREATE TABLE IF NOT EXISTS genero (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

--- ============================================
--- TITULO
--- ============================================
CREATE TABLE IF NOT EXISTS titulo (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nome               TEXT NOT NULL,
    usuario            TEXT REFERENCES usuario(email),
    data_lancamento    TEXT,
    estado_conservacao TEXT,
    descricao          TEXT,
    ativo              INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

-- ============================================
-- AUTOR_TITULO
-- ============================================
CREATE TABLE IF NOT EXISTS autor_titulo (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo INTEGER NOT NULL REFERENCES titulo(id) ON DELETE CASCADE,
    autor  INTEGER NOT NULL REFERENCES autor(id)  ON DELETE CASCADE,
    UNIQUE (titulo, autor)
);

-- ============================================
-- GENERO_TITULO
-- ============================================
CREATE TABLE IF NOT EXISTS genero_titulo (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo INTEGER NOT NULL REFERENCES titulo(id) ON DELETE CASCADE,
    genero INTEGER NOT NULL REFERENCES genero(id) ON DELETE CASCADE,
    UNIQUE (titulo, genero)
);

-- ============================================
-- FAVORITO
-- ============================================
CREATE TABLE IF NOT EXISTS favorito (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT    NOT NULL REFERENCES usuario(email) ON DELETE CASCADE,
    titulo  INTEGER NOT NULL REFERENCES titulo(id)     ON DELETE CASCADE,
    UNIQUE (usuario, titulo)
);

-- ============================================
-- PROPOSTA
-- ============================================
CREATE TABLE IF NOT EXISTS proposta (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    interessado     TEXT NOT NULL REFERENCES usuario(email),
    titulo_desejado INTEGER NOT NULL REFERENCES titulo(id),
    observacao      TEXT,
    data_criacao    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    situacao        TEXT NOT NULL DEFAULT 'pendente' CHECK (situacao IN ('pendente','aceita','recusada','cancelada')),
    ativo        INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

-- ============================================
-- TITULO_OFERECIDO
-- ============================================
CREATE TABLE IF NOT EXISTS titulo_oferecido (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    proposta INTEGER NOT NULL REFERENCES proposta(id) ON DELETE CASCADE,
    titulo   INTEGER NOT NULL REFERENCES titulo(id),
    UNIQUE (proposta, titulo)
);

-- ============================================
-- INDICES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_titulo_usuario       ON titulo(usuario);
CREATE INDEX IF NOT EXISTS idx_proposta_interessado ON proposta(interessado);

-- Unicidade só entre ativos (soft delete)
CREATE UNIQUE INDEX IF NOT EXISTS uq_autor_nome_ativo  ON autor(nome)  WHERE ativo = 1;
CREATE UNIQUE INDEX IF NOT EXISTS uq_genero_nome_ativo ON genero(nome) WHERE ativo = 1;

-- ============================================
-- MASSA DE DADOS (SEED)
-- ============================================

-- 1) USUÁRIOS ---------------------------------------------------
INSERT INTO usuario (email, senha_hash, nome, telefone, cep) VALUES
    -- senha_hash = SHA-256 das senhas ana123, bruno123, carla123 e diego123
    ('ana@example.com',   'e82827b00b2ca8620beb37f879778c082b292a52270390cff35b6fe3157f4e8b', 'Ana Souza',    '(11) 90000-0001', '01001-000'),
    ('bruno@example.com', '956cd9e97c44cbb5c9f18ccf258bb3ea0fbac91d027d2ac9489185f531478242', 'Bruno Lima',   '(11) 90000-0002', '04538-133'),
    ('carla@example.com', 'e408145e7fc3f031d5aa3b08710d0eddabf61cb11864822af9b16b92c0c9c576', 'Carla Mendes', '(21) 90000-0003', '20040-020'),
    ('diego@example.com', 'd68089c77e65ee87eb9504f68212289f6dcb758fae1955a824018a67c5cb2e2f', 'Diego Rocha',  '(31) 90000-0004', '30130-010');

-- 2) AUTORES ----------------------------------------------------
INSERT INTO autor (id, nome) VALUES
    (1, 'Machado de Assis'),
    (2, 'Homero'),
    (3, 'Aluísio Azevedo'),
    (4, 'Neil Gaiman'),
    (5, 'Terry Pratchett'),
    (6, 'George Orwell'),
    (7, 'Sun Tzu'),
    (8, 'J. R. R. Tolkien');

-- 3) GÊNEROS ----------------------------------------------------
INSERT INTO genero (id, nome) VALUES
    (1, 'Romance'),
    (2, 'Épico'),
    (3, 'Fantasia'),
    (4, 'Comédia'),
    (5, 'Distopia'),
    (6, 'Filosofia');

-- 4) TÍTULOS ----------------------------------------------------
INSERT INTO titulo (id, nome, usuario, data_lancamento, estado_conservacao, descricao) VALUES
    (1, 'Dom Casmurro',                    'ana@example.com',   '1899',      'bom',         'Edição de bolso.'),
    (2, 'Memórias Póstumas de Brás Cubas', 'bruno@example.com', '1881',      'regular',     'Algumas páginas grifadas.'),
    (3, 'Ilíada',                          'carla@example.com', 'VIII a.C.', 'novo',        'Tradução em versos.'),
    (4, 'Odisseia',                        'ana@example.com',   'VIII a.C.', 'bom',         ''),
    (5, 'O Cortiço',                       'diego@example.com', '1890',      'desgastado',  'Capa solta.'),
    (6, 'Belas Maldições',                 'bruno@example.com', '1990',      'novo',        ''),
    (7, '1984',                            'carla@example.com', '1949',      'bom',         ''),
    (8, 'A Arte da Guerra',                'diego@example.com', 'V a.C.',    'regular',     ''),
    (9, 'A Sociedade do Anel',             'ana@example.com',   '1954',      'novo',        'Capa dura.');

-- 5) AUTOR_TITULO (N:N) ----------------------------------------
INSERT INTO autor_titulo (titulo, autor) VALUES
    (1, 1),  -- Dom Casmurro              > Machado de Assis
    (2, 1),  -- Memórias Póstumas         > Machado de Assis
    (3, 2),  -- Ilíada                    > Homero
    (4, 2),  -- Odisseia                  > Homero
    (5, 3),  -- O Cortiço                 > Aluísio Azevedo
    (6, 4),  -- Belas Maldições           > Neil Gaiman
    (6, 5),  -- Belas Maldições           > Terry Pratchett
    (7, 6),  -- 1984                      > George Orwell
    (8, 7),  -- A Arte da Guerra          > Sun Tzu
    (9, 8);  -- A Sociedade do Anel       > Tolkien

-- 6) GENERO_TITULO (N:N) ---------------------------------------
INSERT INTO genero_titulo (titulo, genero) VALUES
    (1, 1),  -- Dom Casmurro              > Romance
    (2, 1),  -- Memórias Póstumas         > Romance
    (3, 2),  -- Ilíada                    > Épico
    (4, 2),  -- Odisseia                  > Épico
    (5, 1),  -- O Cortiço                 > Romance
    (6, 3),  -- Belas Maldições           > Fantasia
    (6, 4),  -- Belas Maldições           > Comédia
    (7, 5),  -- 1984                      > Distopia
    (8, 6),  -- A Arte da Guerra          > Filosofia
    (9, 3);  -- A Sociedade do Anel       > Fantasia

-- 7) FAVORITOS --------------------------------------------------
INSERT INTO favorito (usuario, titulo) VALUES
    ('ana@example.com',   7),  -- Ana favoritou 1984
    ('diego@example.com', 3),  -- Diego favoritou Ilíada
    ('bruno@example.com', 9);  -- Bruno favoritou A Sociedade do Anel

-- 8) PROPOSTAS --------------------------------------------------
INSERT INTO proposta (id, interessado, titulo_desejado, observacao, situacao) VALUES
    (1, 'bruno@example.com', 1, 'Troco o Brás Cubas pelo Dom Casmurro.', 'pendente'),  -- quer o Dom Casmurro
    (2, 'carla@example.com', 8, 'Topa trocar pelo 1984?',                 'pendente');  -- quer A Arte da Guerra

-- 9) TITULOS OFERECIDOS -----------------------------------------
INSERT INTO titulo_oferecido (proposta, titulo) VALUES
    (1, 2),  -- Proposta 1 oferece o título 2 (Brás Cubas)
    (2, 7);  -- Proposta 2 oferece o título 7 (1984)
