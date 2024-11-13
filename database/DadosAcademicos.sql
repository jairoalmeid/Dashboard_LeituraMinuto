CREATE DATABASE nilopecanha

-- Criação da tabela para armazenamento dos dados Situação de Matrícula, extraídos do Dashboard da PNP
CREATE TABLE situacao_matricula (
    ano INTEGER NOT NULL,
    unidade VARCHAR(100) NOT NULL,
    subeixo_tecnologico VARCHAR(100),
    tipo_de_curso VARCHAR(50),
    nome_do_curso VARCHAR(100),
    tipo_de_oferta VARCHAR(50),
    modalidade_de_ensino VARCHAR(50),
    turno_do_curso VARCHAR(50),
    situacao VARCHAR(50),
    fluxo_escolar VARCHAR(50),
    fluxo_retido VARCHAR(50),
    matriculas INTEGER
);

-- Criação da tabela para armazenamento dos dados Curso, Matrícula e Oferta, extraídos do Dashboard da PNP
CREATE TABLE curso_matricula_oferta (
    ano INTEGER NOT NULL,
    unidade VARCHAR(100) NOT NULL,
    eixo_tecnologico VARCHAR(100),
    subeixo_tecnologico VARCHAR(100),
    tipo_de_curso VARCHAR(50),
    nome_do_curso VARCHAR(100),
    turno_do_curso VARCHAR(50),
    tipo_de_oferta VARCHAR(50),
    unidades INTEGER,
    cursos INTEGER,
    matriculas INTEGER,
    matriculas_equivalentes NUMERIC(10, 2),
    vagas INTEGER,
    inscritos INTEGER,
    ingressantes INTEGER,
    concluintes INTEGER
);

-- Criação da tabela para armazenamento dos dados Racial, Renda e Sexo, extraídos do Dashboard da PNP
CREATE TABLE classificacao_racial_renda_sexo (
    ano INTEGER NOT NULL,
    classificacao_racial VARCHAR(50),
    renda_familiar VARCHAR(50),
    sexo VARCHAR(10),
    faixa_etaria VARCHAR(20),
    unidade VARCHAR(100) NOT NULL,
    eixo_tecnologico VARCHAR(100),
    subeixo_tecnologico VARCHAR(100),
    tipo_de_curso VARCHAR(50),
    nome_do_curso VARCHAR(100),
    tipo_de_oferta VARCHAR(50),
    modalidade_de_ensino VARCHAR(50),
    turno_do_curso VARCHAR(50),
    matriculas INTEGER,
    vagas INTEGER,
    ingressantes INTEGER,
    concluintes INTEGER
);