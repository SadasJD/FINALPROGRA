import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2025'
    
    # Configuración para Laragon MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Admin123'  
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'ecuador_routes'
    
    # URI de conexión MySQL
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    )
    
    # Fallback a SQLite si MySQL no está disponible
    SQLALCHEMY_DATABASE_URI_SQLITE = 'sqlite:///ecuador_routes.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
