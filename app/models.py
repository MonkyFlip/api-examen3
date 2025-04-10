from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    username = db.Column(db.String(50), nullable=False)  # Nombre del usuario
    email = db.Column(db.String(100), unique=True, nullable=False)  # Correo único
    password = db.Column(db.String(255), nullable=False)  # Contraseña (en texto plano, inicialmente)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Fecha de creación automática

    def to_dict(self):
        """Convierte el modelo a un diccionario para serialización JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }