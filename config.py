import os


class ConfiguracaoProjeto:
    """Configuracoes basicas para executar o prototipo Flask localmente."""

    SECRET_KEY = os.getenv("TRIX_SECRET_KEY", "chave-simples-do-prototipo")
    DEBUG = os.getenv("TRIX_DEBUG", "true").lower() == "true"
