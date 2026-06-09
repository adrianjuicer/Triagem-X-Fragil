"""
seed.py — popula o banco com dados iniciais de desenvolvimento.
Chamado pelo iniciar_trix.py. NÃO faz parte da entrega final.
Cria o banco MySQL, recria as tabelas e insere dados de demonstração.
"""

from sqlalchemy import create_engine, text
from db import engine, SessionLocal, Base
import models


# -------------------------------------------------------
# IDs não-sequenciais (dificulta adivinhação via URL)
# -------------------------------------------------------
ID = {
    # usuários
    "admin":        3847291,
    "suporte.ti":   5129463,
    "dra.ana":      7284016,
    "dr.bruno":     2938471,
    "dra.clara":    6104827,
    "dr.diego":     4792013,
    "dra.fernanda": 8361504,
    "dr.gustavo":   1958420,
    # pacientes
    "lucas":        52836174,
    "sofia":        71930483,
    "miguel":       36402917,
    "laura":        87159263,
    "enzo":         20947381,
    "valentina":    63821094,
    "pedro":        49175038,
    "isabela":      72618403,
    "rafael":       30891547,
    "helena":       54739218,
    "davi":         81260475,
    "manuela":      19382046,
}

# Avaliações (8 dígitos, não sequenciais)
AV = [
    91847203, 63729481, 40183629, 75038163, 28471930, 51903748,
    83620491, 17294853, 39847102, 72613840, 50392719, 84170362,
    26951838, 41837294, 65093470, 30728495, 84910368, 16309470,
    92714830, 48036192, 71592834, 53740613, 29184370, 60478310,
]

# Sintomas presentes por avaliação (ID 11 = Macroorquidismo, só sexo M)
SINTOMAS = {
    AV[0]:  [1, 4, 7, 9, 11, 12],
    AV[1]:  [1, 4, 7, 9, 10, 11, 12],
    AV[2]:  [3, 5],
    AV[3]:  [2, 3, 4],
    AV[4]:  [2, 3, 5, 7],
    AV[5]:  [2, 3, 5, 7, 10],
    AV[6]:  [2, 4, 7],
    AV[7]:  [2, 4, 7, 12],
    AV[8]:  [4, 11, 12],
    AV[9]:  [1, 3, 5, 9],
    AV[10]: [1, 5, 6],
    AV[11]: [2, 3, 9],
    AV[12]: [3, 5, 6],
    AV[13]: [4, 10, 11, 12],
    AV[14]: [2, 3, 4, 12],
    AV[15]: [2, 3, 4, 8, 12],
    AV[16]: [3, 5, 7],
    AV[17]: [3, 5, 7, 10, 12],
    AV[18]: [2, 3, 8],
    AV[19]: [2, 3, 4, 8],
    AV[20]: [5, 6, 8],
    AV[21]: [1, 4, 11],
    AV[22]: [2, 4, 7, 12],
    AV[23]: [2, 3, 4, 9, 12],
}


# -------------------------------------------------------
# Ponto de entrada
# -------------------------------------------------------

def resetar_banco():
    """Cria o banco, recria todas as tabelas e popula com dados iniciais."""
    print("      Criando banco de dados...")
    _criar_banco()
    print("      Recriando tabelas via SQLAlchemy...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _popular(db)
        db.commit()
        print("      Banco populado com sucesso!")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _criar_banco():
    """Drop + create do banco 'trix' via SQLAlchemy (sem depender do cliente mysql)."""
    # engine.url é o objeto URL com senha real — str(engine.url) mascara a senha como ***
    url_servidor = engine.url.set(database="")
    admin_engine = create_engine(url_servidor, pool_pre_ping=True)
    with admin_engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS trix"))
        conn.execute(text(
            "CREATE DATABASE trix "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        ))
        conn.commit()
    admin_engine.dispose()
    engine.dispose()


# -------------------------------------------------------
# Inserções
# -------------------------------------------------------

def _popular(db):
    _usuarios(db)
    _sintomas(db)
    _pacientes(db)
    _avaliacoes(db)
    _avaliacao_sintomas(db)


def _usuarios(db):
    db.add_all([
        models.Usuario(id=ID["admin"],        login="admin",        nome_completo="Administrador de TI",    email="admin@trix.local",        senha="admin123",    perfil="administrador"),
        models.Usuario(id=ID["suporte.ti"],   login="suporte.ti",   nome_completo="Marina Oliveira",         email="suporte@trix.local",      senha="suporte123",  perfil="administrador"),
        models.Usuario(id=ID["dra.ana"],      login="dra.ana",      nome_completo="Dra. Ana Souza",          email="ana@trix.local",           senha="ana123",      perfil="medico"),
        models.Usuario(id=ID["dr.bruno"],     login="dr.bruno",     nome_completo="Dr. Bruno Lima",          email="bruno@trix.local",         senha="bruno123",    perfil="medico"),
        models.Usuario(id=ID["dra.clara"],    login="dra.clara",    nome_completo="Dra. Clara Mendes",       email="clara@trix.local",         senha="clara123",    perfil="medico"),
        models.Usuario(id=ID["dr.diego"],     login="dr.diego",     nome_completo="Dr. Diego Almeida",       email="diego@trix.local",         senha="diego123",    perfil="medico"),
        models.Usuario(id=ID["dra.fernanda"], login="dra.fernanda", nome_completo="Dra. Fernanda Rocha",     email="fernanda@trix.local",      senha="fernanda123", perfil="medico"),
        models.Usuario(id=ID["dr.gustavo"],   login="dr.gustavo",   nome_completo="Dr. Gustavo Nunes",       email="gustavo@trix.local",       senha="gustavo123",  perfil="medico"),
    ])
    db.flush()


def _sintomas(db):
    # Pesos derivados do artigo do Dr. Roberto Hirochi Herai.
    # ID 11 (Macroorquidismo) é referenciado diretamente em schemas.py.
    db.add_all([
        models.Sintoma(id=1,  descricao="Atraso na fala",                                              peso_m=0.1400, peso_f=0.0100),
        models.Sintoma(id=2,  descricao="Dificuldades de aprendizagem",                                peso_m=0.1800, peso_f=0.2800),
        models.Sintoma(id=3,  descricao="Déficit de atenção",                                          peso_m=0.1700, peso_f=0.1200),
        models.Sintoma(id=4,  descricao="Deficiência intelectual (DI)",                                peso_m=0.3200, peso_f=0.2000),
        models.Sintoma(id=5,  descricao="Hiperatividade",                                              peso_m=0.1200, peso_f=0.0400),
        models.Sintoma(id=6,  descricao="Agressividade",                                               peso_m=0.0100, peso_f=0.0200),
        models.Sintoma(id=7,  descricao="Evita contato visual",                                        peso_m=0.0600, peso_f=0.0800),
        models.Sintoma(id=8,  descricao="Evita contato físico",                                        peso_m=0.0400, peso_f=0.0700),
        models.Sintoma(id=9,  descricao="Movimentos intencionais, repetitivos e rítmicos",             peso_m=0.1700, peso_f=0.0500),
        models.Sintoma(id=10, descricao="Hiperflexibilidade articular (hipermobilidade)",              peso_m=0.1900, peso_f=0.0400),
        models.Sintoma(id=11, descricao="Macroorquidismo",                                             peso_m=0.2600, peso_f=None),
        models.Sintoma(id=12, descricao="Rosto alongado, mandíbula proeminente e/ou orelhas de abano", peso_m=0.2900, peso_f=0.0900),
    ])
    db.flush()


def _pacientes(db):
    # Todos são menores de idade (estudo pediátrico de Síndrome do X Frágil).
    # Campos obrigatórios para menores: email, usuario_responsavel, telefone_responsavel.
    from datetime import date
    db.add_all([
        models.Paciente(id=ID["lucas"],     nome="Lucas Pereira Martins",     cpf="90000000001", email="lucas.pereira@example.com",    telefone="11994001001", usuario_responsavel="Ana Pereira Martins",     telefone_responsavel="11985001001", data_nascimento=date(2015,  3, 12), sexo="M"),
        models.Paciente(id=ID["sofia"],     nome="Sofia Almeida Costa",       cpf="90000000002", email="sofia.almeida@example.com",     telefone="21994001002", usuario_responsavel="Carla Almeida Costa",    telefone_responsavel="21985001002", data_nascimento=date(2016,  7, 28), sexo="F"),
        models.Paciente(id=ID["miguel"],    nome="Miguel Santos Oliveira",    cpf="90000000003", email="miguel.santos@example.com",     telefone="31994001003", usuario_responsavel="Jose Santos Oliveira",   telefone_responsavel="31985001003", data_nascimento=date(2014, 11,  5), sexo="M"),
        models.Paciente(id=ID["laura"],     nome="Laura Ribeiro Ferreira",    cpf="90000000004", email="laura.ribeiro@example.com",     telefone="41994001004", usuario_responsavel="Paula Ribeiro Ferreira", telefone_responsavel="41985001004", data_nascimento=date(2017,  2, 19), sexo="F"),
        models.Paciente(id=ID["enzo"],      nome="Enzo Carvalho Lima",        cpf="90000000005", email="enzo.carvalho@example.com",     telefone="51994001005", usuario_responsavel="Roberto Carvalho Lima",  telefone_responsavel="51985001005", data_nascimento=date(2018,  9,  3), sexo="M"),
        models.Paciente(id=ID["valentina"], nome="Valentina Costa Rocha",     cpf="90000000006", email="valentina.costa@example.com",   telefone="61994001006", usuario_responsavel="Fernanda Costa Rocha",   telefone_responsavel="61985001006", data_nascimento=date(2019, 12, 14), sexo="F"),
        models.Paciente(id=ID["pedro"],     nome="Pedro Henrique Nascimento", cpf="90000000007", email="pedro.nascimento@example.com",  telefone="71994001007", usuario_responsavel="Marcos Nascimento",      telefone_responsavel="71985001007", data_nascimento=date(2013,  5, 21), sexo="M"),
        models.Paciente(id=ID["isabela"],   nome="Isabela Monteiro Araujo",   cpf="90000000008", email="isabela.monteiro@example.com",  telefone="81994001008", usuario_responsavel="Sandra Monteiro Araujo", telefone_responsavel="81985001008", data_nascimento=date(2016,  1, 30), sexo="F"),
        models.Paciente(id=ID["rafael"],    nome="Rafael Barbosa Cardoso",    cpf="90000000009", email="rafael.cardoso@example.com",    telefone="11994001009", usuario_responsavel="Paulo Barbosa Cardoso",  telefone_responsavel="11985001009", data_nascimento=date(2012, 10,  8), sexo="M"),
        models.Paciente(id=ID["helena"],    nome="Helena Martins Duarte",     cpf="90000000010", email="helena.duarte@example.com",     telefone="21994001010", usuario_responsavel="Renata Martins Duarte",  telefone_responsavel="21985001010", data_nascimento=date(2018,  4, 17), sexo="F"),
        models.Paciente(id=ID["davi"],      nome="Davi Ribeiro Gomes",        cpf="90000000011", email="davi.ribeiro@example.com",      telefone="31994001011", usuario_responsavel="Silvia Ribeiro Gomes",   telefone_responsavel="31985001011", data_nascimento=date(2015,  8, 26), sexo="M"),
        models.Paciente(id=ID["manuela"],   nome="Manuela Fernandes Lopes",   cpf="90000000012", email="manuela.lopes@example.com",     telefone="41994001012", usuario_responsavel="Lucia Fernandes Lopes",  telefone_responsavel="41985001012", data_nascimento=date(2017,  6,  9), sexo="F"),
    ])
    db.flush()


def _avaliacoes(db):
    from datetime import datetime
    U, P = ID, ID
    dados = [
        (AV[0],  U["dra.ana"],      P["lucas"],     "2026-01-15 09:10", 1.2400, True,  "Responsável relata atraso importante na fala e dificuldade de interação social."),
        (AV[1],  U["dr.bruno"],     P["lucas"],     "2026-04-10 14:30", 1.4300, True,  "Reavaliação com manutenção de sinais físicos e comportamentais relevantes."),
        (AV[2],  U["dr.bruno"],     P["sofia"],     "2026-01-20 10:40", 0.1600, False, "Queixa inicial de desatenção em ambiente escolar, sem outros sinais marcantes."),
        (AV[3],  U["dr.bruno"],     P["sofia"],     "2026-05-02 08:50", 0.6000, True,  "Escola relata piora de aprendizagem e necessidade de apoio pedagógico frequente."),
        (AV[4],  U["dra.clara"],    P["miguel"],    "2026-02-05 15:20", 0.5300, True,  "Acompanhamento inicial por dificuldade de aprendizagem e inquietação."),
        (AV[5],  U["dra.ana"],      P["miguel"],    "2026-05-06 11:00", 0.7200, True,  "Segunda opinião clínica com sinais adicionais observados durante consulta."),
        (AV[6],  U["dr.diego"],     P["laura"],     "2026-02-11 09:35", 0.5600, True,  "Responsável informa atraso escolar e comportamento social reservado."),
        (AV[7],  U["dr.diego"],     P["laura"],     "2026-04-18 13:45", 0.6500, True,  "Reavaliação confirma persistência dos sinais e orienta investigação complementar."),
        (AV[8],  U["dra.fernanda"], P["enzo"],      "2026-02-19 16:10", 0.8700, True,  "Triagem motivada por agitação, dificuldade de atenção e sinais físicos observados."),
        (AV[9],  U["dra.clara"],    P["enzo"],      "2026-05-10 09:25", 0.6000, True,  "Consulta compartilhada com novos sintomas motores relatados pela família."),
        (AV[10], U["dr.gustavo"],   P["valentina"], "2026-03-01 10:05", 0.0700, False, "Primeira triagem com poucos sinais presentes e desenvolvimento global preservado."),
        (AV[11], U["dr.gustavo"],   P["valentina"], "2026-05-12 15:15", 0.4500, False, "Retorno por queixa escolar persistente, ainda sem atingir limiar de recomendação."),
        (AV[12], U["dra.ana"],      P["pedro"],     "2026-03-08 08:30", 0.3000, False, "Histórico familiar informado, mas poucos sinais clínicos presentes na triagem."),
        (AV[13], U["dra.ana"],      P["pedro"],     "2026-05-15 10:20", 1.0600, True,  "Reavaliação amplia registro de sinais físicos e comportamentais."),
        (AV[14], U["dr.bruno"],     P["isabela"],   "2026-03-13 11:50", 0.6900, True,  "Paciente encaminhada pela escola por dificuldade de aprendizagem persistente."),
        (AV[15], U["dr.diego"],     P["isabela"],   "2026-05-04 14:05", 0.7600, True,  "Avaliação compartilhada para revisar sinais cognitivos e sensoriais."),
        (AV[16], U["dra.clara"],    P["rafael"],    "2026-03-21 09:00", 0.3500, False, "Consulta inicial com sinais leves e sem recomendação imediata."),
        (AV[17], U["dra.clara"],    P["rafael"],    "2026-05-17 16:40", 0.8300, True,  "Retorno mostra ampliação dos sintomas e necessidade de investigação."),
        (AV[18], U["dr.diego"],     P["helena"],    "2026-03-27 13:10", 0.4700, False, "Queixa de aprendizagem e sensibilidade ao toque em ambiente escolar."),
        (AV[19], U["dr.gustavo"],   P["helena"],    "2026-05-18 08:45", 0.6700, True,  "Reavaliação com nova informação de atraso cognitivo em relatório externo."),
        (AV[20], U["dra.fernanda"], P["davi"],      "2026-04-03 15:00", 0.1700, False, "Triagem por comportamento agitado, sem achados clínicos suficientes."),
        (AV[21], U["dra.fernanda"], P["davi"],      "2026-05-08 11:35", 0.7200, True,  "Retorno com atenção prejudicada e sinais clínicos adicionais observados."),
        (AV[22], U["dr.gustavo"],   P["manuela"],   "2026-04-12 09:45", 0.6500, True,  "Paciente com histórico escolar sugestivo e sinais observados na consulta."),
        (AV[23], U["dr.bruno"],     P["manuela"],   "2026-05-16 13:20", 0.7400, True,  "Avaliação de apoio confirma indicação de teste genético confirmatório."),
    ]
    for (id_av, id_usr, id_pac, data_str, score, rec, obs) in dados:
        db.add(models.Avaliacao(
            id=id_av, id_usuario=id_usr, id_paciente=id_pac,
            data_avaliacao=datetime.strptime(data_str, "%Y-%m-%d %H:%M"),
            score_calculado=score, recomendacao=rec, observacoes=obs,
        ))
    db.flush()


def _avaliacao_sintomas(db):
    for id_av, ids_sintomas in SINTOMAS.items():
        for id_sintoma in ids_sintomas:
            db.add(models.AvaliacaoSintoma(
                id_avaliacao=id_av, id_sintoma=id_sintoma, presente=True,
            ))
    db.flush()


if __name__ == "__main__":
    resetar_banco()
