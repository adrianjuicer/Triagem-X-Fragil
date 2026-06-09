-- -------------------------------------------------------
-- SETUP DO BANCO
-- Recria o schema (database) trix do zero, garantindo idempotencia.
--
-- NAO cria usuario aqui de proposito: cada maquina conecta com o usuario
-- privilegiado que ja possui (ex.: root nos notebooks da PUC, ou o usuario
-- local de cada um). As credenciais ficam no .env de cada maquina, fora do
-- versionamento. Veja .env.example.
--
-- Rode este script com um usuario que tenha permissao de criar databases.
-- -------------------------------------------------------

DROP DATABASE IF EXISTS trix;
CREATE DATABASE trix
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
