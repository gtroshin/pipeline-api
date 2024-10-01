from flask import Flask
from flask_httpauth import HTTPTokenAuth
from config import API_KEY

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    if token == API_KEY:
        return True
    return False


def create_app():
    app = Flask(__name__)
    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)
    return app
