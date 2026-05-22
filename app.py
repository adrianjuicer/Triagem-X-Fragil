from flask import Flask

from config import ConfiguracaoProjeto
from controllers.principal_controller import principal_blueprint


app = Flask(__name__)
app.config.from_object(ConfiguracaoProjeto)

app.register_blueprint(principal_blueprint)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], use_reloader=False)
