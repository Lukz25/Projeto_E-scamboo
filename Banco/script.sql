

CREATE TABLE usuario(
    email TEXT PRIMARY KEY,
    senha_hash TEXT,
    nome TEXT,
    telefone TEXT,
    CEP TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE -- Soft Delete
);

CREATE TABLE autor(
    id SERIAL PRIMARY KEY,
    nome TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE -- Soft Delete
);         

CREATE TABLE genero(
    id SERIAL PRIMARY KEY,
    nome TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE -- Soft Delete
);

CREATE TABLE titulo(
    id SERIAL PRIMARY KEY,
    usuario TEXT REFERENCES usuario(email),
    data_lancamento DATE,
    estado_conservacao TEXT,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE -- Soft Delete
);

CREATE TABLE titulo_autor(
    id SERIAL PRIMARY KEY,
    titulo INT REFERENCES titulo(id),
    autor INT REFERENCES autor(id)
);

CREATE TABLE titulo_genero(
    id SERIAL PRIMARY KEY,
    titulo INT REFERENCES titulo(id),
    genero INT REFERENCES genero(id)
);

CREATE TABLE favorito(
    id SERIAL PRIMARY KEY,
    usuario TEXT REFERENCES usuario(email),
    titulo INT REFERENCES 
);

CREATE TABLE proposta(
    id SERIAL PRIMARY KEY,
    interessado TEXT REFERENCES usuario(email),
    observacao TEXT,
    data_criacao DATE DEFAULT NOW(),
    situacao TEXT, -- Proposta aceita, recusada, cancelada
    ativo BOOLEAN NOT NULL DEFAULT TRUE -- Soft Delete
);

CREATE TABLE titulo_oferecido(
    id SERIAL PRIMARY KEY,
    proposta INT REFERENCES proposta(id),
    titulo INT REFERENCES titulo(id)
);

CREATE TABLE registro_titulo(
    id SERIAL PRIMARY KEY,
    titulo INT REFERENCES titulo(id),
    dado_antes JSONB,
    dado_deposi JSONB,
    alterado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE registro_proposta(
    id SERIAL PRIMARY KEY,
    proposta INT REFERENCES proposta(id),
    dado_antes JSONB,
    dado_deposi JSONB,
    alterado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


