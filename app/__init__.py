from flask import Flask
from flask_httpauth import HTTPTokenAuth
from app.config import API_KEY

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    """
    Verifies the provided token against the API key.

    Args:
        token (str): The token to be verified.

    Returns:
        bool: True if the token matches the API key, False otherwise.
    """
    if token == API_KEY:
        return True
    return False


def create_app():
    """
    Creates and configures the Flask application.

    This function sets up the Flask application, registers the routes blueprint,
    and returns the configured app instance.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)
    return app
