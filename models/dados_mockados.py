SINTOMAS_DISPONIVEIS = [
    {"id": 1, "descricao": "Deficiência intelectual"},
    {"id": 2, "descricao": "Face alongada/orelhas"},
    {"id": 3, "descricao": "Macroorquidismo"},
    {"id": 4, "descricao": "Hipermobilidade articular"},
    {"id": 5, "descricao": "Dificuldades de aprendizagem"},
    {"id": 6, "descricao": "Déficit de atenção"},
    {"id": 7, "descricao": "Movimentos repetitivos"},
    {"id": 8, "descricao": "Atraso na fala"},
    {"id": 9, "descricao": "Hiperatividade"},
    {"id": 10, "descricao": "Evita contato visual"},
    {"id": 11, "descricao": "Evita contato físico"},
    {"id": 12, "descricao": "Agressividade"},
]


USUARIOS_CADASTRADOS = [
    {"id": 1, "login": "admin", "perfil": "Administrador"},
    {"id": 2, "login": "dra.ana", "perfil": "Profissional de Saúde"},
]


AVALIACOES_EXEMPLO = [
    {
        "data": "10/04/2026",
        "cpf": "000.000.000-01",
        "rg": "11.111.111-1",
        "paciente": "João Silva",
        "sexo": "M",
        "usuario": "dra.ana",
        "sintomas": [
            "Deficiência intelectual",
            "Face alongada/orelhas",
            "Macroorquidismo",
            "Hiperatividade",
        ],
        "score": "0.89",
        "recomendacao": "Recomendado ao teste genético confirmatório",
    },
    {
        "data": "11/04/2026",
        "cpf": "000.000.000-02",
        "rg": "22.222.222-2",
        "paciente": "Maria Souza",
        "sexo": "F",
        "usuario": "dra.ana",
        "sintomas": [
            "Dificuldades de aprendizagem",
            "Déficit de atenção",
        ],
        "score": "0.40",
        "recomendacao": "Não recomendado ao teste genético confirmatório",
    },
]
