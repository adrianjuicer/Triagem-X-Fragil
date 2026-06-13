-- -------------------------------------------------------
-- SETUP DO BANCO — Recria o schema (database) trix do zero.
-- -------------------------------------------------------

DROP DATABASE IF EXISTS trix;
CREATE DATABASE trix
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
