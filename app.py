from flask import Flask
from config import Config
from models import db

# Importamos las rutas desde la carpeta routes
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Intentar conectar a MQL primero, luego SQLite como fallback
    try:
        # Probar conexión MySQL
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print("✅ Conectado a MySQL/MariaDB (Laragon)")
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        print("🔄 Usando SQLite como fallback...")
        # Cambiar a SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_SQLITE']
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print("✅ Conectado a SQLite")
    
    # Registramos los blueprints
    register_blueprints(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)