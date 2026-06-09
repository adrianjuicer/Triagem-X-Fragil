from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(120), unique=True, nullable=False, index=True)
    nome_completo = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(
        Enum("administrador", "medico"),
        nullable=False,
        default="medico",
        server_default="medico",
    )
    data_criacao = Column(DateTime, nullable=False, server_default=func.now())

    avaliacoes = relationship("Avaliacao", back_populates="usuario")


class Paciente(Base):
    __tablename__ = "paciente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    telefone = Column(String(11), nullable=True)
    telefone_responsavel = Column(String(11), nullable=True)
    usuario_responsavel = Column(String(100), nullable=True)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(1), nullable=False)

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="paciente",
        cascade="all, delete-orphan",
    )


class Sintoma(Base):
    __tablename__ = "sintoma"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), unique=True, nullable=False)
    peso_m = Column(Numeric(7, 4), nullable=False)
    peso_f = Column(Numeric(7, 4), nullable=True)

    avaliacoes = relationship("AvaliacaoSintoma", back_populates="sintoma")


class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_paciente = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False)
    data_avaliacao = Column(DateTime, nullable=False, server_default=func.now())
    score_calculado = Column(Numeric(7, 4), nullable=False, default=0)
    recomendacao = Column(Boolean, nullable=False, default=False)
    observacoes = Column(Text, nullable=True)

    usuario = relationship("Usuario", back_populates="avaliacoes")
    paciente = relationship("Paciente", back_populates="avaliacoes")
    sintomas = relationship(
        "AvaliacaoSintoma",
        back_populates="avaliacao",
        cascade="all, delete-orphan",
    )


class AvaliacaoSintoma(Base):
    __tablename__ = "avaliacao_sintomas"

    id = Column(Integer, primary_key=True, index=True)
    id_avaliacao = Column(
        Integer,
        ForeignKey("avaliacao.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_sintoma = Column(Integer, ForeignKey("sintoma.id"), nullable=False)
    presente = Column(Boolean, nullable=False, default=True)

    avaliacao = relationship("Avaliacao", back_populates="sintomas")
    sintoma = relationship("Sintoma", back_populates="avaliacoes")
