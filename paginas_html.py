"""Funções de renderização das páginas HTML do TriX usando Jinja2."""

from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


BASE_DIR = Path(__file__).resolve().parent

templates = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def _render(nome_template: str, **ctx) -> str:
    return templates.get_template(nome_template).render(**ctx)


def nome_perfil(perfil: str) -> str:
    return "Administrador" if perfil == "administrador" else "Funcionário da Saúde"


templates.globals["nome_perfil"] = nome_perfil


# -------------------------------------------------------
# Páginas
# -------------------------------------------------------

def pagina_login(erro: str = "") -> str:
    if erro == "login":
        erro = "Login ou senha inválidos."
    return _render("login.html", erro=erro)


def pagina_menu(sessao: dict) -> str:
    return _render("menu.html", sessao=sessao, pagina_atual="/menu")


def pagina_triagem(sessao: dict, sintomas, erro: str = "", erro_campo: str = "", dados: dict = None) -> str:
    return _render(
        "triagem.html",
        sessao=sessao, pagina_atual="/triagem",
        sintomas=sintomas, erro=erro, erro_campo=erro_campo, dados=dados or {},
        hoje=date.today().isoformat(),
    )


def pagina_resultado_triagem(sessao: dict, resultado) -> str:
    return _render(
        "resultado_triagem.html",
        sessao=sessao, pagina_atual="/triagem",
        resultado=resultado,
    )


def pagina_detalhe_paciente(sessao: dict, registros) -> str:
    return _render(
        "paciente_detalhe.html",
        sessao=sessao, pagina_atual="/relatorios",
        registros=registros,
    )


def pagina_relatorios_admin(sessao: dict, avaliacoes, filtros: dict, aviso: str = "") -> str:
    return _render(
        "relatorios_admin.html",
        sessao=sessao, pagina_atual="/relatorios",
        avaliacoes=avaliacoes, filtros=filtros, aviso=aviso,
    )


def pagina_relatorios_saude(sessao: dict, avaliacoes, filtros: dict, aviso: str = "") -> str:
    return _render(
        "relatorios_saude.html",
        sessao=sessao, pagina_atual="/relatorios",
        avaliacoes=avaliacoes, filtros=filtros, aviso=aviso,
    )


def pagina_cadastro_usuario(sessao: dict, erro: str = "", sucesso: str = "") -> str:
    return _render(
        "cadastro_usuario.html",
        sessao=sessao, pagina_atual="/usuarios/novo",
        erro=erro, sucesso=sucesso,
    )


def pagina_usuarios(sessao: dict, usuarios) -> str:
    return _render(
        "usuarios.html",
        sessao=sessao, pagina_atual="/usuarios",
        usuarios=usuarios,
    )
