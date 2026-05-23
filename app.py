from flask import Flask

from controllers.principal_controller import principal_blueprint


app = Flask(__name__)
app.register_blueprint(principal_blueprint)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
