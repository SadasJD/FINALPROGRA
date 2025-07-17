from services.interfaces import UserServiceInterface
from models import User, db

class UserService(UserServiceInterface):
    def create_user(self, username):
        """Crea un nuevo usuario"""
        if self.user_exists(username):
            return None
        
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user(self, username):
        """Obtiene un usuario por su username"""
        return User.query.filter_by(username=username).first()
    
    def user_exists(self, username):
        """Verifica si un usuario existe"""
        return User.query.filter_by(username=username).first() is not None
    
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        return User.query.all()
