from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app import db
from app.routes.auth_routes import auth_ns
from app.routes.user_routes import user_ns
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Configuración de Swagger/OpenAPI
    api = Api(
        app,
        title="API de Usuarios",
        version="1.0",
        description="Documentación de los endpoints disponibles",
        doc='/docs'  # Exponer documentación en esta ruta
    )

    # Agregar Namespaces (rutas y lógica)
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(user_ns, path='/users')

    # Ruta principal: Simple mensaje de saludo
    @app.route('/', methods=['GET'])
    def index():
        return {"message": "Bienvenido a la API de Usuarios. Explora la documentación en /docs o consulta los usuarios en /users."}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)