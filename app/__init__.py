from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')

    # Inicializar la base de datos
    db.init_app(app)

    return app