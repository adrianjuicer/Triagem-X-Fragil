from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

import models
import schemas


LIMIAR_M = 0.56
LIMIAR_F = 0.55

PERFIS_VALIDOS = {"administrador", "medico"}


# -------------------------------------------------------
# Helpers internos
# -------------------------------------------------------

def _so_digitos(valor: str) -> str:
    return "".join(c for c in (valor or "") if c.isdigit())


def _validar_perfil(perfil: str) -> str:
    p = (perfil or "").strip().lower()
    if p not in PERFIS_VALIDOS:
        raise HTTPException(status_code=400, detail="Perfil de acesso inválido.")
    return p


# -------------------------------------------------------
# Usuários
# -------------------------------------------------------

def autenticar_usuario(db: Session, dados: schemas.LoginRequest) -> models.Usuario:
    usuario = (
        db.query(models.Usuario)
        .filter(
            models.Usuario.login == dados.login.strip(),
            models.Usuario.senha == dados.senha,
        )
        .first()
    )
    if not usuario:
        raise HTTPException(status_code=401, detail="Login ou senha inválidos.")
    return usuario


def obter_usuario_por_id(db: Session, usuario_id: int) -> Optional[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def listar_usuarios(db: Session) -> List[models.Usuario]:
    return db.query(models.Usuario).order_by(models.Usuario.id).all()


def criar_usuario(db: Session, dados: schemas.UsuarioCreate) -> models.Usuario:
    perfil = _validar_perfil(dados.perfil)
    login  = dados.login.strip()
    nome   = (dados.nome_completo or login).strip()
    email  = (dados.email or f"{login}@trix.local").strip().lower()

    novo = models.Usuario(login=login, nome_completo=nome, email=email,
                          senha=dados.senha, perfil=perfil)
    db.add(novo)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Login ou e-mail já cadastrado.") from exc
    db.refresh(novo)
    return novo


# -------------------------------------------------------
# Sintomas
# -------------------------------------------------------

def listar_sintomas(db: Session) -> List[models.Sintoma]:
    return db.query(models.Sintoma).order_by(models.Sintoma.id).all()


# -------------------------------------------------------
# Triagens / Avaliações
# -------------------------------------------------------

def obter_avaliacao_por_id(db: Session, avaliacao_id: int) -> Optional[models.Avaliacao]:
    return (
        db.query(models.Avaliacao)
        .options(
            joinedload(models.Avaliacao.paciente),
            joinedload(models.Avaliacao.usuario),
            joinedload(models.Avaliacao.sintomas).joinedload(models.AvaliacaoSintoma.sintoma),
        )
        .filter(models.Avaliacao.id == avaliacao_id)
        .first()
    )


def listar_avaliacoes_do_paciente(db: Session, paciente_id: int) -> List[models.Avaliacao]:
    """Todas as avaliações de um paciente (qualquer médico), mais recente primeiro."""
    return (
        db.query(models.Avaliacao)
        .options(
            joinedload(models.Avaliacao.paciente),
            joinedload(models.Avaliacao.usuario),
            joinedload(models.Avaliacao.sintomas).joinedload(models.AvaliacaoSintoma.sintoma),
        )
        .filter(models.Avaliacao.id_paciente == paciente_id)
        .order_by(models.Avaliacao.data_avaliacao.desc(), models.Avaliacao.id.desc())
        .all()
    )


def listar_avaliacoes(
    db: Session,
    id_usuario: int,
    perfil: str,
    cpf: Optional[str] = None,
    paciente_id: Optional[int] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    score_min: Optional[float] = None,
    score_max: Optional[float] = None,
    sexo: Optional[str] = None,
) -> List[models.Avaliacao]:
    perfil = _validar_perfil(perfil)
    query = (
        db.query(models.Avaliacao)
        .options(
            joinedload(models.Avaliacao.paciente),
            joinedload(models.Avaliacao.usuario),
            joinedload(models.Avaliacao.sintomas).joinedload(models.AvaliacaoSintoma.sintoma),
        )
        .join(models.Avaliacao.paciente)
        .order_by(models.Avaliacao.data_avaliacao.desc(), models.Avaliacao.id.desc())
    )

    if perfil == "administrador":
        if cpf:
            cpf_limpo = _so_digitos(cpf)
            if cpf_limpo:
                query = query.filter(models.Paciente.cpf.contains(cpf_limpo))
            else:
                nome_busca = cpf.strip().lower()
                if nome_busca:
                    query = query.filter(models.Paciente.nome.ilike(f"%{nome_busca}%"))
    else:
        cpf_limpo = _so_digitos(cpf) if cpf else ""
        # Busca por CPF completo (11 dígitos) mostra histórico de toda a clínica (handoff).
        # Sem CPF completo, mostra apenas os atendimentos do próprio médico.
        if len(cpf_limpo) != 11:
            query = query.filter(models.Avaliacao.id_usuario == id_usuario)
        if cpf:
            if cpf_limpo:
                query = query.filter(models.Paciente.cpf.contains(cpf_limpo))
            else:
                nome_busca = cpf.strip().lower()
                if nome_busca:
                    query = query.filter(models.Paciente.nome.ilike(f"%{nome_busca}%"))

    if data_inicio:
        try:
            query = query.filter(
                models.Avaliacao.data_avaliacao >= datetime.strptime(data_inicio, "%Y-%m-%d")
            )
        except ValueError:
            pass

    if data_fim:
        try:
            dt_fim = datetime.strptime(data_fim, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            query = query.filter(models.Avaliacao.data_avaliacao <= dt_fim)
        except ValueError:
            pass

    if score_min is not None:
        query = query.filter(models.Avaliacao.score_calculado >= score_min)
    if score_max is not None:
        query = query.filter(models.Avaliacao.score_calculado <= score_max)
    if sexo and sexo.upper() in ("M", "F"):
        query = query.filter(models.Paciente.sexo == sexo.upper())

    return query.all()


def criar_triagem(db: Session, dados: schemas.TriagemCreate, id_usuario: int) -> models.Avaliacao:
    usuario = obter_usuario_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário responsável não encontrado.")

    ids_sintomas = sorted(set(dados.ids_sintomas_marcados))
    sintomas = (
        db.query(models.Sintoma)
        .filter(models.Sintoma.id.in_(ids_sintomas))
        .order_by(models.Sintoma.id)
        .all()
    )
    if len(sintomas) != len(ids_sintomas):
        raise HTTPException(status_code=400, detail="Um ou mais sintomas informados são inválidos.")

    try:
        paciente = _obter_ou_criar_paciente(db, dados)
        score, recomendada = _calcular_score(paciente.sexo, sintomas)

        avaliacao = models.Avaliacao(
            usuario=usuario,
            paciente=paciente,
            data_avaliacao=datetime.now(),
            score_calculado=score,
            recomendacao=recomendada,
            observacoes=dados.observacoes,
        )
        db.add(avaliacao)
        db.flush()

        for sintoma in sintomas:
            db.add(models.AvaliacaoSintoma(avaliacao=avaliacao, sintoma=sintoma, presente=True))

        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail="E-mail já cadastrado para outro paciente.") from exc

    db.refresh(avaliacao)
    return avaliacao


# -------------------------------------------------------
# Formatação de dados para templates
# -------------------------------------------------------

def formatar_cpf(cpf: str) -> str:
    d = _so_digitos(cpf)
    if len(d) != 11:
        return cpf
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


def formatar_telefone(telefone: Optional[str]) -> str:
    d = _so_digitos(telefone or "")
    if len(d) == 10:
        return f"({d[:2]}) {d[2:6]}-{d[6:]}"
    if len(d) == 11:
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"
    return telefone or ""


def avaliacao_para_formulario(avaliacao: models.Avaliacao) -> dict:
    """Converte uma avaliação salva em dict para pré-preencher o formulário de triagem."""
    p = avaliacao.paciente
    return {
        "nome":                  p.nome,
        "cpf":                   formatar_cpf(p.cpf),
        "data_nascimento":       p.data_nascimento.isoformat(),
        "sexo":                  p.sexo,
        "email":                 p.email or "",
        "telefone":              formatar_telefone(p.telefone),
        "usuario_responsavel":   p.usuario_responsavel or "",
        "telefone_responsavel":  formatar_telefone(p.telefone_responsavel),
        "observacoes":           avaliacao.observacoes or "",
        "ids_sintomas_marcados": [item.id_sintoma for item in avaliacao.sintomas if item.presente],
    }


class Registro:
    """Objeto simples de leitura para os templates consumirem dados de avaliação."""
    def __init__(self, **kwargs):
        for chave, valor in kwargs.items():
            setattr(self, chave, valor)


def avaliacao_para_registro(avaliacao: models.Avaliacao, esconder_dados_paciente: bool = False) -> Registro:
    """Converte uma avaliação ORM num Registro simples para os templates."""
    sintomas_presentes = [
        item.sintoma.descricao
        for item in avaliacao.sintomas
        if item.presente and item.sintoma
    ]
    limiar = LIMIAR_M if avaliacao.paciente.sexo == "M" else LIMIAR_F

    return Registro(
        id=avaliacao.id,
        paciente_id=avaliacao.paciente.id,
        data=avaliacao.data_avaliacao.strftime("%d/%m/%Y"),
        data_nascimento=avaliacao.paciente.data_nascimento.isoformat(),
        cpf=""          if esconder_dados_paciente else formatar_cpf(avaliacao.paciente.cpf),
        paciente=""     if esconder_dados_paciente else avaliacao.paciente.nome,
        email=""        if esconder_dados_paciente else (avaliacao.paciente.email or ""),
        telefone=""     if esconder_dados_paciente else formatar_telefone(avaliacao.paciente.telefone),
        telefone_responsavel="" if esconder_dados_paciente else formatar_telefone(avaliacao.paciente.telefone_responsavel),
        usuario_responsavel=""  if esconder_dados_paciente else (avaliacao.paciente.usuario_responsavel or ""),
        sexo=avaliacao.paciente.sexo,
        usuario=avaliacao.usuario.nome_completo,
        usuario_id=avaliacao.id_usuario,
        sintomas=sintomas_presentes,
        ids_sintomas=[item.id_sintoma for item in avaliacao.sintomas if item.presente],
        score=round(avaliacao.score_calculado or 0, 4),
        limiar=limiar,
        recomendada=bool(avaliacao.recomendacao),
        observacoes=avaliacao.observacoes or "",
    )


# -------------------------------------------------------
# Funções internas (não exportadas)
# -------------------------------------------------------

def _obter_ou_criar_paciente(db: Session, dados: schemas.TriagemCreate) -> models.Paciente:
    paciente = db.query(models.Paciente).filter(models.Paciente.cpf == dados.cpf).first()
    if paciente:
        # CPF já existe: usa o registro atual sem sobrescrever.
        # Isso preserva o histórico do paciente quando um novo profissional
        # faz uma triagem usando o mesmo CPF.
        return paciente

    paciente = models.Paciente(
        nome=dados.nome.strip(),
        cpf=dados.cpf,
        email=dados.email,
        telefone=dados.telefone,
        telefone_responsavel=dados.telefone_responsavel,
        usuario_responsavel=dados.usuario_responsavel,
        data_nascimento=dados.data_nascimento,
        sexo=dados.sexo.upper(),
    )
    db.add(paciente)
    db.flush()
    return paciente


def _calcular_score(sexo: str, sintomas: List[models.Sintoma]) -> tuple[float, bool]:
    if sexo == "M":
        score  = sum(s.peso_m for s in sintomas)
        limiar = LIMIAR_M
    else:
        score  = sum(s.peso_f or 0 for s in sintomas)
        limiar = LIMIAR_F
    score_arredondado = round(score, 4)
    return score_arredondado, score_arredondado >= limiar
