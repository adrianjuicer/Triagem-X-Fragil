import os
from datetime import date
from typing import List, Optional
from urllib.parse import quote

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

import crud
import paginas_html
import schemas
from db import SessionLocal, engine, Base
import models


# -------------------------------------------------------
# Inicialização do banco (BioCadastro style)
# -------------------------------------------------------
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Conectado ao banco de dados com sucesso.")
except OperationalError as e:
    import sys
    print("\nERRO: não foi possível conectar ao banco de dados.")
    print("Verifique se o MySQL está rodando e se já rodou o iniciar_trix.py.")
    print(f"Detalhe técnico: {e.orig}\n")
    sys.exit(1)

Base.metadata.create_all(bind=engine)

_secret_key = os.getenv("SECRET_KEY")
if not _secret_key:
    raise RuntimeError(
        "SECRET_KEY não definida. Configure o arquivo .env antes de iniciar."
    )

app = FastAPI(title="TriX", version="4.0.0", docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=_secret_key)
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------------------------------
# Banco de dados
# -------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------
# Sessão — lida do request.session (server-side)
# -------------------------------------------------------

def extrair_sessao(request: Request) -> Optional[dict]:
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    return {
        "usuario_id": usuario_id,
        "perfil":     request.session.get("perfil"),
        "login":      request.session.get("login"),
        "nome":       request.session.get("nome"),
    }


def redirecionar_login():
    return RedirectResponse("/", status_code=303)


# -------------------------------------------------------
# Helpers de validação de erro (formulário de triagem)
# -------------------------------------------------------

def _extrair_erro_validacao(erro) -> tuple[str, str]:
    """Extrai mensagem e campo de um erro de validação Pydantic ou HTTPException."""
    campo = ""
    if isinstance(erro, ValidationError):
        primeiro = erro.errors()[0]
        detalhe  = primeiro.get("msg", "Dados inválidos.")
        loc      = primeiro.get("loc", ())
        if loc:
            campo = str(loc[-1])
        if detalhe.startswith("Value error, "):
            detalhe = detalhe[len("Value error, "):]
    else:
        detalhe = getattr(erro, "detail", str(erro))

    # Erros de regras cruzadas (model_validator) chegam sem campo definido.
    if not campo:
        d = detalhe.lower()
        if "macroorquidismo" in d:
            campo = "sexo"
        elif "usuário responsável" in d or "usuario responsavel" in d:
            campo = "usuario_responsavel"
        elif "telefone do responsável" in d or "telefone do responsavel" in d:
            campo = "telefone_responsavel"

    return detalhe, campo


# -------------------------------------------------------
# Login / Logout
# -------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def exibir_login(erro: Optional[str] = None):
    return paginas_html.pagina_login(erro=erro or "")


@app.post("/login")
def processar_login(
    request: Request,
    login: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        usuario = crud.autenticar_usuario(db, schemas.LoginRequest(login=login, senha=senha))
    except HTTPException:
        return RedirectResponse("/?erro=login", status_code=303)

    request.session.clear()
    request.session["usuario_id"] = usuario.id
    request.session["perfil"]     = usuario.perfil
    request.session["login"]      = usuario.login
    request.session["nome"]       = usuario.nome_completo
    return RedirectResponse("/menu", status_code=303)


@app.get("/sair")
def sair(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# -------------------------------------------------------
# Menu
# -------------------------------------------------------

@app.get("/menu", response_class=HTMLResponse)
def exibir_menu(request: Request):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    return paginas_html.pagina_menu(sessao)


# -------------------------------------------------------
# Triagem
# -------------------------------------------------------

@app.get("/triagem", response_class=HTMLResponse)
def exibir_triagem(
    request: Request,
    copiar_de: Optional[int] = None,
    db: Session = Depends(get_db),
):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()

    dados = {}
    if copiar_de:
        avaliacao = crud.obter_avaliacao_por_id(db, copiar_de)
        if avaliacao:
            eh_dono  = avaliacao.id_usuario == sessao["usuario_id"]
            eh_admin = sessao["perfil"] == "administrador"
            if eh_dono or eh_admin:
                dados = crud.avaliacao_para_formulario(avaliacao)

    sintomas = crud.listar_sintomas(db)
    return paginas_html.pagina_triagem(sessao, sintomas, dados=dados)


@app.post("/triagem")
def processar_triagem(
    request: Request,
    nome:                  str           = Form(...),
    cpf:                   str           = Form(...),
    data_nascimento:       date          = Form(...),
    sexo:                  str           = Form(...),
    email:                 Optional[str] = Form(None),
    telefone:              Optional[str] = Form(None),
    usuario_responsavel:   Optional[str] = Form(None),
    telefone_responsavel:  Optional[str] = Form(None),
    observacoes:           Optional[str] = Form(None),
    ids_sintomas_marcados: List[int]     = Form(default=[]),
    db: Session = Depends(get_db),
):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()

    dados_formulario = {
        "nome": nome, "cpf": cpf,
        "data_nascimento": data_nascimento.isoformat(), "sexo": sexo,
        "email": email or "", "telefone": telefone or "",
        "usuario_responsavel": usuario_responsavel or "",
        "telefone_responsavel": telefone_responsavel or "",
        "observacoes": observacoes or "",
        "ids_sintomas_marcados": ids_sintomas_marcados,
    }

    try:
        triagem_data = schemas.TriagemCreate(
            nome=nome, cpf=cpf, email=email, telefone=telefone or None,
            usuario_responsavel=usuario_responsavel or None,
            telefone_responsavel=telefone_responsavel or None,
            data_nascimento=data_nascimento, sexo=sexo,
            observacoes=observacoes or None,
            ids_sintomas_marcados=ids_sintomas_marcados,
        )
        avaliacao = crud.criar_triagem(db, triagem_data, sessao["usuario_id"])
    except (HTTPException, ValueError, ValidationError) as erro:
        detalhe, campo = _extrair_erro_validacao(erro)
        sintomas = crud.listar_sintomas(db)
        return HTMLResponse(
            paginas_html.pagina_triagem(sessao, sintomas, erro=str(detalhe),
                                        erro_campo=campo, dados=dados_formulario),
            status_code=400,
        )

    return RedirectResponse(f"/triagem/{avaliacao.id}/resultado", status_code=303)


@app.get("/triagem/{avaliacao_id}/resultado", response_class=HTMLResponse)
def exibir_resultado_triagem(avaliacao_id: int, request: Request, db: Session = Depends(get_db)):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()

    avaliacao = crud.obter_avaliacao_por_id(db, avaliacao_id)
    if not avaliacao:
        return RedirectResponse("/relatorios", status_code=303)

    eh_dono  = avaliacao.id_usuario == sessao["usuario_id"]
    eh_admin = sessao["perfil"] == "administrador"
    if not eh_dono and not eh_admin:
        raise HTTPException(status_code=401)

    resultado = crud.avaliacao_para_registro(avaliacao, esconder_dados_paciente=False)
    return paginas_html.pagina_resultado_triagem(sessao, resultado)


# -------------------------------------------------------
# Histórico do paciente
# -------------------------------------------------------

@app.get("/pacientes/{paciente_id}", response_class=HTMLResponse)
def exibir_detalhe_paciente(paciente_id: int, request: Request, db: Session = Depends(get_db)):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()

    avaliacoes_orm = crud.listar_avaliacoes_do_paciente(db, paciente_id)
    if not avaliacoes_orm:
        return RedirectResponse("/relatorios", status_code=303)

    eh_admin             = sessao["perfil"] == "administrador"
    usuario_tem_avaliacao = any(a.id_usuario == sessao["usuario_id"] for a in avaliacoes_orm)
    if not eh_admin and not usuario_tem_avaliacao:
        raise HTTPException(status_code=401)

    registros = [crud.avaliacao_para_registro(a, esconder_dados_paciente=False)
                 for a in avaliacoes_orm]
    return paginas_html.pagina_detalhe_paciente(sessao, registros)


# -------------------------------------------------------
# Relatórios (redirect por perfil)
# -------------------------------------------------------

@app.get("/relatorios")
def redirecionar_relatorios(request: Request):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    destino = "/relatorios_admin" if sessao["perfil"] == "administrador" else "/relatorios_saude"
    return RedirectResponse(destino, status_code=307)


def _extrair_filtros(request: Request) -> dict:
    p = request.query_params
    return {
        "paciente":    p.get("f_paciente", ""),
        "data_inicio": p.get("f_data_inicio", ""),
        "data_fim":    p.get("f_data_fim", ""),
        "score_min":   p.get("f_score_min", ""),
        "score_max":   p.get("f_score_max", ""),
        "sexo":        p.get("f_sexo", ""),
    }


def _score_para_float(valor: str) -> Optional[float]:
    if not valor:
        return None
    try:
        score = float(valor.replace(",", "."))
    except ValueError:
        return None
    return score if 0 <= score <= 2 else None


@app.get("/relatorios_admin", response_class=HTMLResponse)
def exibir_relatorios_admin(request: Request, db: Session = Depends(get_db)):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    if sessao["perfil"] != "administrador":
        return RedirectResponse("/relatorios_saude", status_code=303)

    filtros = _extrair_filtros(request)
    aviso   = request.query_params.get("aviso", "")

    avaliacoes_orm = crud.listar_avaliacoes(
        db, id_usuario=sessao["usuario_id"], perfil="administrador",
        cpf=filtros["paciente"] or None,
        data_inicio=filtros["data_inicio"] or None,
        data_fim=filtros["data_fim"] or None,
        score_min=_score_para_float(filtros["score_min"]),
        score_max=_score_para_float(filtros["score_max"]),
        sexo=filtros["sexo"] or None,
    )
    avaliacoes = [crud.avaliacao_para_registro(a, esconder_dados_paciente=False) for a in avaliacoes_orm]
    return paginas_html.pagina_relatorios_admin(sessao, avaliacoes, filtros, aviso=aviso)


@app.get("/relatorios_saude", response_class=HTMLResponse)
def exibir_relatorios_saude(request: Request, db: Session = Depends(get_db)):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    if sessao["perfil"] == "administrador":
        return RedirectResponse("/relatorios_admin", status_code=303)

    filtros = _extrair_filtros(request)
    aviso   = request.query_params.get("aviso", "")

    avaliacoes_orm = crud.listar_avaliacoes(
        db, id_usuario=sessao["usuario_id"], perfil=sessao["perfil"],
        cpf=filtros["paciente"] or None,
        data_inicio=filtros["data_inicio"] or None,
        data_fim=filtros["data_fim"] or None,
        score_min=_score_para_float(filtros["score_min"]),
        score_max=_score_para_float(filtros["score_max"]),
        sexo=filtros["sexo"] or None,
    )
    avaliacoes = [crud.avaliacao_para_registro(a, esconder_dados_paciente=False) for a in avaliacoes_orm]
    return paginas_html.pagina_relatorios_saude(sessao, avaliacoes, filtros, aviso=aviso)


# -------------------------------------------------------
# Usuários (somente administrador)
# -------------------------------------------------------

@app.get("/usuarios/novo", response_class=HTMLResponse)
def exibir_cadastro_usuario(request: Request):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    if sessao["perfil"] != "administrador":
        raise HTTPException(status_code=401)
    erro    = request.query_params.get("erro", "")
    sucesso = "Usuário cadastrado com sucesso." if request.query_params.get("status") == "ok" else ""
    return paginas_html.pagina_cadastro_usuario(sessao, erro=erro, sucesso=sucesso)


@app.post("/usuarios/salvar")
def criar_usuario_formulario(
    request: Request,
    login:         str = Form(...),
    nome_completo: str = Form(...),
    email:         str = Form(...),
    senha:         str = Form(...),
    perfil:        str = Form(...),
    db: Session = Depends(get_db),
):
    sessao = extrair_sessao(request)
    if not sessao or sessao["perfil"] != "administrador":
        return redirecionar_login()

    try:
        crud.criar_usuario(db, schemas.UsuarioCreate(
            login=login, nome_completo=nome_completo,
            email=email, senha=senha, perfil=perfil,
        ))
        destino = "/usuarios/novo?status=ok"
    except HTTPException as e:
        destino = f"/usuarios/novo?erro={quote(str(e.detail))}"

    return RedirectResponse(destino, status_code=303)


@app.get("/usuarios", response_class=HTMLResponse)
def listar_usuarios_pagina(request: Request, db: Session = Depends(get_db)):
    sessao = extrair_sessao(request)
    if not sessao:
        return redirecionar_login()
    if sessao["perfil"] != "administrador":
        raise HTTPException(status_code=401)
    usuarios = crud.listar_usuarios(db)
    return paginas_html.pagina_usuarios(sessao, usuarios)


# -------------------------------------------------------
# Health check
# -------------------------------------------------------

@app.get("/api/health")
def healthcheck():
    return {"status": "ok", "service": "trix"}
