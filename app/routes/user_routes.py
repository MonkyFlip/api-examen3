from flask_restx import Namespace, Resource
from flask import request
from app.models import User, db

# Definimos el Namespace para usuarios
user_ns = Namespace('users', description='Rutas para manejo de usuarios')

@user_ns.route('/')
class UserList(Resource):
    def get(self):
        """Obtén todos los usuarios en formato JSON"""
        try:
            users = User.query.all()
            users_dict = [user.to_dict() for user in users]
            return users_dict, 200  # Devuelve directamente la lista de usuarios
        except Exception as e:
            return {"message": "Error fetching users", "error": str(e)}, 500

    def post(self):
        """Crear un nuevo usuario"""
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return {"message": "Todos los campos son obligatorios"}, 400

            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return {"message": "Usuario creado exitosamente", "user": new_user.to_dict()}, 201
        except Exception as e:
            return {"message": "Error creando usuario", "error": str(e)}, 500

@user_ns.route('/<int:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        """Obtener un usuario por ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"message": "Usuario no encontrado"}, 404

            return user.to_dict(), 200  # Devuelve directamente los datos del usuario
        except Exception as e:
            return {"message": "Error obteniendo usuario", "error": str(e)}, 500

    def put(self, user_id):
        """Actualizar un usuario existente"""
        try:
            data = request.get_json()
            user = User.query.get(user_id)

            if not user:
                return {"message": "Usuario no encontrado"}, 404

            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)

            db.session.commit()
            return {"message": "Usuario actualizado exitosamente", "user": user.to_dict()}, 200
        except Exception as e:
            return {"message": "Error actualizando usuario", "error": str(e)}, 500

    def delete(self, user_id):
        """Eliminar un usuario por ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"message": "Usuario no encontrado"}, 404

            db.session.delete(user)
            db.session.commit()
            return {"message": "Usuario eliminado exitosamente"}, 200
        except Exception as e:
            return {"message": "Error eliminando usuario", "error": str(e)}, 500