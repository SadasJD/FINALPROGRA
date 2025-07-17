from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con consultas de rutas
    route_queries = db.relationship('RouteQuery', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class RouteQuery(db.Model):
    __tablename__ = 'route_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    start_city = db.Column(db.String(100), nullable=False)
    end_city = db.Column(db.String(100), nullable=False)
    best_route = db.Column(db.Text, nullable=False)  # JSON string
    total_distance = db.Column(db.Numeric(10, 2), nullable=False)
    query_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_route_as_list(self):
        """Convierte la ruta JSON a lista de Python"""
        return json.loads(self.best_route)
    
    def set_route_from_list(self, route_list):
        """Convierte una lista de Python a JSON para almacenar"""
        self.best_route = json.dumps(route_list)
    
    def __repr__(self):
        return f'<RouteQuery {self.start_city} -> {self.end_city}>'
