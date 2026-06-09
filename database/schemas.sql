
CREATE DATABASE IF NOT EXISTS trix
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE trix;


-- -------------------------------------------------------
-- TABELA: usuario
-- Perfil controlado por ENUM, sem tabela roles separada.
-- -------------------------------------------------------
CREATE TABLE usuario (
  id            INT PRIMARY KEY AUTO_INCREMENT,
  login         VARCHAR(120) NOT NULL UNIQUE,
  nome_completo VARCHAR(255) NOT NULL,
  email         VARCHAR(255) NOT NULL UNIQUE,
  senha         VARCHAR(255) NOT NULL,
  perfil        ENUM('administrador', 'medico') NOT NULL DEFAULT 'medico',
  data_criacao  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP

);

-- -------------------------------------------------------
-- TABELA: paciente
-- data_nascimento no lugar de idade (idade fica desatualizada).
-- -------------------------------------------------------
CREATE TABLE paciente (
  id                 INT PRIMARY KEY AUTO_INCREMENT,
  nome               VARCHAR(255) NOT NULL,
  cpf                VARCHAR(11) NOT NULL UNIQUE,
  email              VARCHAR(255) UNIQUE,
  telefone           VARCHAR(11),
  telefone_responsavel VARCHAR(11),
  usuario_responsavel VARCHAR(100),
  data_nascimento    DATE NOT NULL,
  sexo               CHAR(1) NOT NULL,

  CONSTRAINT chk_sexo CHECK (sexo IN ('M', 'F'))
);

-- -------------------------------------------------------
-- TABELA: sintoma
-- Apenas descricao + pesos. nome_sintoma removido.
-- -------------------------------------------------------
CREATE TABLE sintoma (
  id             INT PRIMARY KEY AUTO_INCREMENT,
  descricao      VARCHAR(255) NOT NULL,
  peso_m         DECIMAL(7,4) NOT NULL,
  peso_f         DECIMAL(7,4)
);

-- -------------------------------------------------------
-- TABELA: avaliacao
-- Guarda o resultado clínico por paciente/usuario/data.
-- id_usuario e id_paciente possuem FOREIGN KEY fisica.
-- classificacao_recomendacao REMOVIDA — gerar no template:
--   {% if avaliacao.recomendacao %}Recomendado{% else %}Não recomendado{% endif %}
-- -------------------------------------------------------
CREATE TABLE avaliacao (
  id                INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario        INT NOT NULL,
  id_paciente       INT NOT NULL,
  data_avaliacao    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  score_calculado   DECIMAL(7,4),
  recomendacao      BOOLEAN,
  observacoes       TEXT,

  CONSTRAINT fk_avaliacao_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  CONSTRAINT fk_avaliacao_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES paciente (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- -------------------------------------------------------
-- TABELA: avaliacao_sintomas
-- Tabela associativa N:M entre avaliacao e sintoma.
-- id_avaliacao e id_sintoma possuem FOREIGN KEY fisica.
-- presente = TRUE se o sintoma foi marcado pelo profissional.
-- -------------------------------------------------------
CREATE TABLE avaliacao_sintomas (
  id             INT PRIMARY KEY AUTO_INCREMENT,
  id_avaliacao   INT NOT NULL,
  id_sintoma     INT NOT NULL,
  presente       BOOLEAN NOT NULL,

  CONSTRAINT fk_avaliacao_sintomas_avaliacao
    FOREIGN KEY (id_avaliacao)
    REFERENCES avaliacao (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

  CONSTRAINT fk_avaliacao_sintomas_sintoma
    FOREIGN KEY (id_sintoma)
    REFERENCES sintoma (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- -------------------------------------------------------
-- SEED: sintomas (12 sintomas do checklist clínico)
-- Pesos derivados do artigo do Dr. Roberto Hirochi Herai.
-- -------------------------------------------------------
INSERT INTO sintoma (descricao, peso_m, peso_f) VALUES
  ('Atraso na fala',                                               0.1400, 0.0100),
  ('Dificuldades de aprendizagem',                                 0.1800, 0.2800),
  ('Déficit de atenção',                                           0.1700, 0.1200),
  ('Deficiência intelectual (DI)',                                 0.3200, 0.2000),
  ('Hiperatividade',                                               0.1200, 0.0400),
  ('Agressividade',                                                0.0100, 0.0200),
  ('Evita contato visual',                                         0.0600, 0.0800),
  ('Evita contato físico',                                         0.0400, 0.0700),
  ('Movimentos intencionais, repetitivos e rítmicos',              0.1700, 0.0500),
  ('Hiperflexibilidade articular (hipermobilidade)',               0.1900, 0.0400),
  ('Macroorquidismo',                                              0.2600, NULL),
  ('Rosto alongado, mandíbula proeminente e/ou orelhas de abano',  0.2900, 0.0900);

-- -------------------------------------------------------
-- SEED: usuario administrador padrão para primeiro acesso
-- Troque a senha antes de colocar em uso.
-- -------------------------------------------------------
-- INSERT INTO usuario (login, senha, perfil) VALUES ---
-- ('admin', 'trocar_antes_de_usar', 'administrador') ---
