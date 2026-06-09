from datetime import date
import re
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


NOME_RE  = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ '\-]+$")
LOGIN_RE = re.compile(r"^[A-Za-z0-9._-]+$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# -------------------------------------------------------
# Helpers de validação reutilizados por vários schemas
# -------------------------------------------------------

def _limpar(valor: Optional[str]) -> Optional[str]:
    """Remove espaços das bordas; devolve None se vazio."""
    if valor is None:
        return None
    return valor.strip() or None


def _so_digitos(valor: Optional[str]) -> Optional[str]:
    if valor is None:
        return None
    return "".join(c for c in valor if c.isdigit()) or None


def _validar_nome(valor: Optional[str], campo: str) -> Optional[str]:
    v = _limpar(valor)
    if v is None:
        return None
    if not (2 <= len(v) <= 100):
        raise ValueError(f"{campo} deve ter entre 2 e 100 caracteres.")
    if not NOME_RE.fullmatch(v):
        raise ValueError(f"{campo} deve conter apenas letras, espaços, hífen e apóstrofo.")
    return v


def _validar_email(valor: Optional[str]) -> Optional[str]:
    v = _limpar(valor)
    if v is None:
        return None
    if not EMAIL_RE.fullmatch(v):
        raise ValueError("E-mail inválido.")
    return v.lower()


def _validar_telefone(valor: Optional[str]) -> Optional[str]:
    digitos = _so_digitos(_limpar(valor))
    if digitos is None:
        return None
    if len(digitos) not in (10, 11):
        raise ValueError("Telefone deve conter 10 ou 11 números.")
    return digitos


# -------------------------------------------------------
# Login
# -------------------------------------------------------

class LoginRequest(BaseModel):
    login: str = Field(min_length=2, max_length=120)
    senha: str = Field(min_length=3, max_length=255)


# -------------------------------------------------------
# Cadastro de usuário
# -------------------------------------------------------

class UsuarioCreate(BaseModel):
    login:         str            = Field(min_length=2, max_length=120)
    senha:         str            = Field(min_length=3, max_length=255)
    perfil:        str
    nome_completo: Optional[str]  = None
    email:         Optional[str]  = None

    @field_validator("login")
    @classmethod
    def validar_login(cls, v: str) -> str:
        v = v.strip()
        if not LOGIN_RE.fullmatch(v):
            raise ValueError("Login deve conter apenas letras, números, ponto, hífen ou underline.")
        return v

    @field_validator("nome_completo")
    @classmethod
    def validar_nome_completo(cls, v: Optional[str]) -> Optional[str]:
        return _validar_nome(v, "Nome")

    @field_validator("email")
    @classmethod
    def validar_email_usuario(cls, v: Optional[str]) -> Optional[str]:
        return _validar_email(v)


# -------------------------------------------------------
# Triagem (formulário principal)
# -------------------------------------------------------

class TriagemCreate(BaseModel):
    nome:                  str           = Field(min_length=2, max_length=100)
    cpf:                   str
    email:                 Optional[str] = None
    telefone:              Optional[str] = None
    usuario_responsavel:   Optional[str] = Field(default=None, max_length=100)
    telefone_responsavel:  Optional[str] = None
    data_nascimento:       date
    sexo:                  str
    observacoes:           Optional[str] = Field(default=None, max_length=2000)
    ids_sintomas_marcados: List[int]     = Field(default_factory=list)

    @field_validator("nome")
    @classmethod
    def validar_nome_paciente(cls, v: str) -> str:
        resultado = _validar_nome(v, "Nome do paciente")
        if resultado is None:
            raise ValueError("Nome do paciente é obrigatório.")
        return resultado

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, v: str) -> str:
        digitos = _so_digitos(v)
        if not digitos or len(digitos) != 11:
            raise ValueError("CPF deve conter 11 números.")
        return digitos

    @field_validator("email")
    @classmethod
    def validar_email_paciente(cls, v: Optional[str]) -> str:
        resultado = _validar_email(v)
        if resultado is None:
            raise ValueError("E-mail é obrigatório.")
        return resultado

    @field_validator("usuario_responsavel")
    @classmethod
    def validar_usuario_responsavel(cls, v: Optional[str]) -> Optional[str]:
        return _validar_nome(v, "Usuário responsável")

    @field_validator("telefone", "telefone_responsavel")
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        return _validar_telefone(v)

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, v: str) -> str:
        s = v.strip().upper()
        if s not in {"M", "F"}:
            raise ValueError("Sexo deve ser M ou F.")
        return s

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: date) -> date:
        if v.year < 1900 or v.year > date.today().year:
            raise ValueError("Ano de nascimento inválido.")
        if v > date.today():
            raise ValueError("Data de nascimento não pode estar no futuro.")
        return v

    @model_validator(mode="after")
    def validar_regras_clinicas(self):
        # Sintoma ID 11 = Macroorquidismo: exclusivo do sexo masculino
        if self.sexo == "F" and 11 in self.ids_sintomas_marcados:
            raise ValueError("Macroorquidismo é exclusivo para pacientes do sexo masculino.")

        # Paciente menor de idade exige responsável
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        if idade < 18:
            if not self.usuario_responsavel:
                raise ValueError("Usuário responsável é obrigatório para pacientes menores de idade.")
            if not self.telefone_responsavel:
                raise ValueError("Telefone do responsável é obrigatório para pacientes menores de idade.")
        return self
