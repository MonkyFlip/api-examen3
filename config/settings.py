import os

class Config:
    """Configuración general para Flask"""
    # URI de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///:memory:')
    # Deshabilitar el seguimiento de modificaciones (por razones de rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clave secreta para tokens JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave_secreta_predeterminada')
    # Configuración de CORS
    CORS_HEADERS = 'Content-Type'
    # Configuración de Flask-JWT-Extended
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'