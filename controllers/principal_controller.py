from flask import Blueprint, redirect, render_template, request, url_for


principal_blueprint = Blueprint("principal", __name__)


def obter_perfil_atual():
    perfil = request.args.get("perfil")

    if perfil == "administrador":
        return "administrador"

    return "medico"


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


@principal_blueprint.route("/")
def exibir_login():
    """Mostra a primeira tela do sistema."""
    return render_template("index.html", exibir_menu=False, mensagem_erro=None)


@principal_blueprint.route("/login", methods=["POST"])
def entrar_no_sistema():
    """Recebe o formulario de login e leva o usuario para o menu."""
    perfil_escolhido = request.form.get("perfil")

    if perfil_escolhido not in ["administrador", "medico"]:
        return render_template(
            "index.html",
            exibir_menu=False,
            mensagem_erro="Escolha um perfil de acesso.",
        )

    return redirect(url_for("principal.exibir_menu", perfil=perfil_escolhido))


@principal_blueprint.route("/sair")
def sair_do_sistema():
    """Volta para a tela de login."""
    return redirect(url_for("principal.exibir_login"))


@principal_blueprint.route("/menu")
def exibir_menu():
    """Mostra o menu principal do prototipo."""
    return render_template(
        "menu.html",
        pagina_ativa="menu",
        perfil_atual=obter_perfil_atual(),
    )


@principal_blueprint.route("/triagem")
def exibir_triagem():
    """Mostra a tela de cadastro de paciente e checklist."""
    return render_template(
        "triagem.html",
        pagina_ativa="triagem",
        perfil_atual=obter_perfil_atual(),
        sintomas_disponiveis=SINTOMAS_DISPONIVEIS,
        usuarios_cadastrados=USUARIOS_CADASTRADOS,
    )


@principal_blueprint.route("/triagem/salvar", methods=["POST"])
def salvar_triagem():
    """Prototipo visual: volta para relatorios depois do envio."""
    return redirect(url_for("principal.exibir_relatorios", perfil=obter_perfil_atual()))


@principal_blueprint.route("/relatorios")
def exibir_relatorios():
    """Mostra a tela de relatorios do prototipo."""
    return render_template(
        "relatorios.html",
        pagina_ativa="relatorios",
        perfil_atual=obter_perfil_atual(),
        avaliacoes=AVALIACOES_EXEMPLO,
        usuarios_filtro=USUARIOS_CADASTRADOS,
    )


@principal_blueprint.route("/pacientes/buscar", methods=["POST"])
def buscar_paciente():
    """Prototipo visual: mantem o usuario na tela de relatorios."""
    return redirect(url_for("principal.exibir_relatorios", perfil=obter_perfil_atual()))


@principal_blueprint.route("/usuarios/novo")
def exibir_cadastro_usuario():
    """Mostra a tela de cadastro de usuario."""
    return render_template(
        "cadastro_usuario.html",
        pagina_ativa="usuarios",
        perfil_atual=obter_perfil_atual(),
        mensagem_erro=None,
        mensagem_sucesso=None,
    )


@principal_blueprint.route("/usuarios/salvar", methods=["POST"])
def salvar_usuario():
    """Prototipo visual: mostra mensagem simples de cadastro."""
    return render_template(
        "cadastro_usuario.html",
        pagina_ativa="usuarios",
        perfil_atual=obter_perfil_atual(),
        mensagem_erro=None,
        mensagem_sucesso="Usuário cadastrado no protótipo.",
    )


@principal_blueprint.route("/usuarios")
def listar_usuarios():
    """Mostra a tela com usuarios cadastrados."""
    return render_template(
        "lista_usuarios.html",
        pagina_ativa="usuarios",
        perfil_atual=obter_perfil_atual(),
        usuarios=USUARIOS_CADASTRADOS,
        mensagem_erro=None,
    )
