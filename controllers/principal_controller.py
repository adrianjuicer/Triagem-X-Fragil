from flask import Blueprint, redirect, render_template, request, session, url_for

from models import AVALIACOES_EXEMPLO, SINTOMAS_DISPONIVEIS, USUARIOS_CADASTRADOS


principal_blueprint = Blueprint("principal", __name__)


@principal_blueprint.route("/")
def exibir_login():
    """Mostra a primeira tela do sistema."""
    session.clear()
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

    session["perfil_usuario"] = perfil_escolhido
    return redirect(url_for("principal.exibir_menu"))


@principal_blueprint.route("/sair")
def sair_do_sistema():
    """Limpa o acesso atual e volta para o login."""
    session.clear()
    return redirect(url_for("principal.exibir_login"))


@principal_blueprint.route("/menu")
def exibir_menu():
    """Mostra o menu principal do prototipo."""
    return render_template("menu.html", pagina_ativa="menu")


@principal_blueprint.route("/triagem")
def exibir_triagem():
    """Mostra a tela de cadastro de paciente e checklist."""
    return render_template(
        "triagem.html",
        pagina_ativa="triagem",
        sintomas_disponiveis=SINTOMAS_DISPONIVEIS,
        usuarios_cadastrados=USUARIOS_CADASTRADOS,
    )


@principal_blueprint.route("/triagem/salvar", methods=["POST"])
def salvar_triagem():
    """Prototipo visual: volta para relatorios depois do envio."""
    return redirect(url_for("principal.exibir_relatorios"))


@principal_blueprint.route("/relatorios")
def exibir_relatorios():
    """Mostra a tela de relatorios do prototipo."""
    return render_template(
        "relatorios.html",
        pagina_ativa="relatorios",
        avaliacoes=AVALIACOES_EXEMPLO,
        usuarios_filtro=USUARIOS_CADASTRADOS,
    )


@principal_blueprint.route("/pacientes/buscar", methods=["POST"])
def buscar_paciente():
    """Prototipo visual: mantem o usuario na tela de relatorios."""
    return redirect(url_for("principal.exibir_relatorios"))


@principal_blueprint.route("/usuarios/novo")
def exibir_cadastro_usuario():
    """Mostra a tela de cadastro de usuario."""
    return render_template(
        "cadastro_usuario.html",
        pagina_ativa="usuarios",
        mensagem_erro=None,
        mensagem_sucesso=None,
    )


@principal_blueprint.route("/usuarios/salvar", methods=["POST"])
def salvar_usuario():
    """Prototipo visual: mostra mensagem simples de cadastro."""
    return render_template(
        "cadastro_usuario.html",
        pagina_ativa="usuarios",
        mensagem_erro=None,
        mensagem_sucesso="Usuário cadastrado no protótipo.",
    )


@principal_blueprint.route("/usuarios")
def listar_usuarios():
    """Mostra a tela com usuarios cadastrados."""
    return render_template(
        "lista_usuarios.html",
        pagina_ativa="usuarios",
        usuarios=USUARIOS_CADASTRADOS,
        mensagem_erro=None,
    )
