from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models import User

auth_ns = Namespace('auth', description='Rutas para autenticación')

@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        """Autenticar usuario y devolver un token JWT"""
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {"message": "Email and password are required"}, 400

            user = User.query.filter_by(email=email).first()
            if user and user.password == password:  # Nota: En el futuro, usar hashing para contraseñas
                token = create_access_token(identity=user.id)
                return {"access_token": token}, 200
            else:
                return {"message": "Invalid email or password"}, 401
        except Exception as e:
            return {"message": "Error during login", "error": str(e)}, 500