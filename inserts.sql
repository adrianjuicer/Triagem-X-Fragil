USE trix;

-- -------------------------------------------------------
-- LIMPEZA DAS TABELAS (Prevenção de duplicidade)
-- -------------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE avaliacao_sintomas;
TRUNCATE TABLE avaliacao;
TRUNCATE TABLE sintoma;
TRUNCATE TABLE paciente;
TRUNCATE TABLE usuario;
SET FOREIGN_KEY_CHECKS = 1;

-- -------------------------------------------------------
-- CARGA DE USUÁRIOS
-- -------------------------------------------------------
INSERT INTO usuario (id, login, nome_completo, email, senha, perfil) VALUES
(1, 'admin', 'Administrador de TI', 'admin@trix.local', 'admin123', 'administrador'),
(2, 'suporte.ti', 'Marina Oliveira', 'suporte.ti@trix.local', 'suporte123', 'administrador'),
(3, 'dra.ana', 'Dra. Ana Souza', 'ana@trix.local', 'ana123', 'medico'),
(4, 'dr.bruno', 'Dr. Bruno Lima', 'bruno@trix.local', 'bruno123', 'medico'),
(5, 'dra.clara', 'Dra. Clara Mendes', 'clara@trix.local', 'clara123', 'medico'),
(6, 'dr.diego', 'Dr. Diego Almeida', 'diego@trix.local', 'diego123', 'medico'),
(7, 'dra.fernanda', 'Dra. Fernanda Rocha', 'fernanda@trix.local', 'fernanda123', 'medico'),
(8, 'dr.gustavo', 'Dr. Gustavo Nunes', 'gustavo@trix.local', 'gustavo123', 'medico');

-- -------------------------------------------------------
-- CARGA DE PACIENTES
-- -------------------------------------------------------
INSERT INTO paciente (id, nome, cpf, email, telefone, telefone_responsavel, data_nascimento, sexo) VALUES
(1, 'Lucas Pereira Martins', '90000000001', 'lucas.pereira@example.com', '11994001001', '11985001001', '2015-03-12', 'M'),
(2, 'Sofia Almeida Costa', '90000000002', 'sofia.almeida@example.com', '21994001002', '21985001002', '2016-07-28', 'F'),
(3, 'Miguel Santos Oliveira', '90000000003', NULL, '31994001003', '31985001003', '2014-11-05', 'M'),
(4, 'Laura Ribeiro Ferreira', '90000000004', 'laura.ribeiro@example.com', '41994001004', NULL, '2017-02-19', 'F'),
(5, 'Enzo Carvalho Lima', '90000000005', NULL, '51994001005', '51985001005', '2018-09-03', 'M'),
(6, 'Valentina Costa Rocha', '90000000006', 'valentina.costa@example.com', NULL, '61985001006', '2019-12-14', 'F'),
(7, 'Pedro Henrique Nascimento', '90000000007', 'pedro.nascimento@example.com', '71994001007', NULL,          '1985-05-21', 'M'),
(8, 'Isabela Monteiro Araujo', '90000000008', NULL,                           '81994001008', '81985001008', '2016-01-30', 'F'),
(9, 'Rafael Barbosa Cardoso', '90000000009', 'rafael.cardoso@example.com',    '11994001009', NULL,          '1990-10-08', 'M'),
(10, 'Helena Martins Duarte', '90000000010', 'helena.duarte@example.com',     '21994001010', NULL,          '1995-04-17', 'F'),
(11, 'Davi Ribeiro Gomes', '90000000011', NULL,                               '31994001011', '31985001011', '2015-08-26', 'M'),
(12, 'Manuela Fernandes Lopes', '90000000012', 'manuela.lopes@example.com',   '41994001012', NULL,          '1992-06-09', 'F');

-- -------------------------------------------------------
-- CARGA DE SINTOMAS
-- -------------------------------------------------------
INSERT INTO sintoma (id, descricao, peso_m, peso_f) VALUES
(1, 'Atraso na fala', 0.1400, 0.0100),
(2, 'Dificuldades de aprendizagem', 0.1800, 0.2800),
(3, 'Déficit de atenção', 0.1700, 0.1200),
(4, 'Deficiência intelectual (DI)', 0.3200, 0.2000),
(5, 'Hiperatividade', 0.1200, 0.0400),
(6, 'Agressividade', 0.0100, 0.0200),
(7, 'Evita contato visual', 0.0600, 0.0800),
(8, 'Evita contato físico', 0.0400, 0.0700),
(9, 'Movimentos intencionais, repetitivos e rítmicos', 0.1700, 0.0500),
(10, 'Hiperflexibilidade articular (hipermobilidade)', 0.1900, 0.0400),
(11, 'Macroorquidismo', 0.2600, NULL),
(12, 'Rosto alongado, mandíbula proeminente e/ou orelhas de abano', 0.2900, 0.0900);

-- -------------------------------------------------------
-- CARGA DE AVALIAÇÕES
-- Limiares aplicados: masculino >= 0.56 | feminino >= 0.55
-- -------------------------------------------------------
INSERT INTO avaliacao (id, id_usuario, id_paciente, data_avaliacao, score_calculado, recomendacao, observacoes) VALUES
(1, 3, 1, '2026-01-15 09:10:00', 1.2400, 1, 'Responsável relata atraso importante na fala e dificuldade de interação social.'),
(2, 4, 1, '2026-04-10 14:30:00', 1.4300, 1, 'Reavaliação com manutenção de sinais físicos e comportamentais relevantes.'),
(3, 4, 2, '2026-01-20 10:40:00', 0.1600, 0, 'Queixa inicial de desatenção em ambiente escolar, sem outros sinais marcantes.'),
(4, 4, 2, '2026-05-02 08:50:00', 0.6000, 1, 'Escola relata piora de aprendizagem e necessidade de apoio pedagógico frequente.'),
(5, 5, 3, '2026-02-05 15:20:00', 0.5300, 1, 'Acompanhamento inicial por dificuldade de aprendizagem e inquietação.'),
(6, 3, 3, '2026-05-06 11:00:00', 0.7200, 1, 'Segunda opinião clínica com sinais adicionais observados durante consulta.'),
(7, 6, 4, '2026-02-11 09:35:00', 0.5600, 1, 'Responsável informa atraso escolar e comportamento social reservado.'),
(8, 6, 4, '2026-04-18 13:45:00', 0.6500, 1, 'Reavaliação confirma persistência dos sinais e orienta investigação complementar.'),
(9, 7, 5, '2026-02-19 16:10:00', 0.8700, 1, 'Triagem motivada por agitação, dificuldade de atenção e sinais físicos observados.'),
(10, 5, 5, '2026-05-10 09:25:00', 0.6000, 1, 'Consulta compartilhada com novos sintomas motores relatados pela família.'),
(11, 8, 6, '2026-03-01 10:05:00', 0.0700, 0, 'Primeira triagem com poucos sinais presentes e desenvolvimento global preservado.'),
(12, 8, 6, '2026-05-12 15:15:00', 0.4500, 0, 'Retorno por queixa escolar persistente, ainda sem atingir limiar de recomendação.'),
(13, 3, 7, '2026-03-08 08:30:00', 0.3000, 0, 'Histórico familiar informado, mas poucos sinais clínicos presentes na triagem.'),
(14, 3, 7, '2026-05-15 10:20:00', 1.0600, 1, 'Reavaliação amplia registro de sinais físicos e comportamentais.'),
(15, 4, 8, '2026-03-13 11:50:00', 0.6900, 1, 'Paciente encaminhada pela escola por dificuldade de aprendizagem persistente.'),
(16, 6, 8, '2026-05-04 14:05:00', 0.7600, 1, 'Avaliação compartilhada para revisar sinais cognitivos e sensoriais.'),
(17, 5, 9, '2026-03-21 09:00:00', 0.3500, 0, 'Consulta inicial com sinais leves e sem recomendação imediata.'),
(18, 5, 9, '2026-05-17 16:40:00', 0.8300, 1, 'Retorno mostra ampliação dos sintomas e necessidade de investigação.'),
(19, 6, 10, '2026-03-27 13:10:00', 0.4700, 0, 'Queixa de aprendizagem e sensibilidade ao toque em ambiente escolar.'),
(20, 8, 10, '2026-05-18 08:45:00', 0.6700, 1, 'Reavaliação com nova informação de atraso cognitivo em relatório externo.'),
(21, 7, 11, '2026-04-03 15:00:00', 0.1700, 0, 'Triagem por comportamento agitado, sem achados clínicos suficientes.'),
(22, 7, 11, '2026-05-08 11:35:00', 0.7200, 1, 'Retorno com atenção prejudicada e sinais clínicos adicionais observados.'),
(23, 8, 12, '2026-04-12 09:45:00', 0.6500, 1, 'Paciente com histórico escolar sugestivo e sinais observados na consulta.'),
(24, 4, 12, '2026-05-16 13:20:00', 0.7400, 1, 'Avaliação de apoio confirma indicação de teste genético confirmatório.');

-- -------------------------------------------------------
-- RELACIONAMENTO N:M (avaliacao_sintomas)
-- Mesma lógica do Python: insere todos como ausente (0) e marca os presentes como (1)
-- -------------------------------------------------------

-- 1. Cria a matriz base ligando todas as 24 avaliações a todos os 12 sintomas como não marcados (0)
INSERT INTO avaliacao_sintomas (id_avaliacao, id_sintoma, presente)
SELECT a.id, s.id, 0 
FROM avaliacao a CROSS JOIN sintoma s;

-- 2. Atualiza para verdadeiro (1) apenas os sintomas que foram mapeados em suas respectivas consultas
UPDATE avaliacao_sintomas 
SET presente = 1 
WHERE (id_avaliacao = 1 AND id_sintoma IN (1, 4, 7, 9, 11, 12))
   OR (id_avaliacao = 2 AND id_sintoma IN (1, 4, 7, 9, 10, 11, 12))
   OR (id_avaliacao = 3 AND id_sintoma IN (3, 5))
   OR (id_avaliacao = 4 AND id_sintoma IN (2, 3, 4))
   OR (id_avaliacao = 5 AND id_sintoma IN (2, 3, 5, 7))
   OR (id_avaliacao = 6 AND id_sintoma IN (2, 3, 5, 7, 10))
   OR (id_avaliacao = 7 AND id_sintoma IN (2, 4, 7))
   OR (id_avaliacao = 8 AND id_sintoma IN (2, 4, 7, 12))
   OR (id_avaliacao = 9 AND id_sintoma IN (4, 11, 12))
   OR (id_avaliacao = 10 AND id_sintoma IN (1, 3, 5, 9))
   OR (id_avaliacao = 11 AND id_sintoma IN (1, 5, 6))
   OR (id_avaliacao = 12 AND id_sintoma IN (2, 3, 9))
   OR (id_avaliacao = 13 AND id_sintoma IN (3, 5, 6))
   OR (id_avaliacao = 14 AND id_sintoma IN (4, 10, 11, 12))
   OR (id_avaliacao = 15 AND id_sintoma IN (2, 3, 4, 12))
   OR (id_avaliacao = 16 AND id_sintoma IN (2, 3, 4, 8, 12))
   OR (id_avaliacao = 17 AND id_sintoma IN (3, 5, 7))
   OR (id_avaliacao = 18 AND id_sintoma IN (3, 5, 7, 10, 12))
   OR (id_avaliacao = 19 AND id_sintoma IN (2, 3, 8))
   OR (id_avaliacao = 20 AND id_sintoma IN (2, 3, 4, 8))
   OR (id_avaliacao = 21 AND id_sintoma IN (5, 6, 8))
   OR (id_avaliacao = 22 AND id_sintoma IN (1, 4, 11))
   OR (id_avaliacao = 23 AND id_sintoma IN (2, 4, 7, 12))
   OR (id_avaliacao = 24 AND id_sintoma IN (2, 3, 4, 9, 12));