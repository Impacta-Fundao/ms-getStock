from flask import Flask, redirect
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    @app.route("/")
    def raiz():
        redirect("/", code=302)
        return "Hello World"
    return app