from flask import Flask

from config import ConfiguracaoProjeto
from controllers.principal_controller import principal_blueprint
from extensions import inicializar_extensoes


def criar_app():
    """Cria a aplicacao Flask e registra a estrutura MVC inicial."""
    app = Flask(__name__)
    app.config.from_object(ConfiguracaoProjeto)

    inicializar_extensoes(app)
    app.register_blueprint(principal_blueprint)

    return app


app = criar_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], use_reloader=False)
