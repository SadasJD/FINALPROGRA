#!/usr/bin/env python3
"""
Script para configurar la base de datos en Laragon MySQL
"""

import pymysql
import sys

def test_mysql_connection():
    """Probar conexión a MySQL/MariaDB de Laragon"""
    try:
        # Configuración por defecto de Laragon
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Admin123',  # Contraseña de Laragon
        )
        print("✅ Conexión a MySQL/MariaDB exitosa")
        
        # Crear base de datos si no existe
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecuador_routes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute("USE ecuador_routes")
            print("✅ Base de datos 'ecuador_routes' creada/verificada")
        
        connection.commit()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        print("💡 Asegúrate de que Laragon esté ejecutándose")
        return False

def test_app_connection():
    """Probar conexión desde la aplicación Flask"""
    try:
        from app import app
        with app.app_context():
            from models import db, User
            
            # Probar crear tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Probar insertar usuario de prueba
            test_user = User(username='test_db_connection')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Usuario de prueba insertado")
            
            # Verificar que el usuario existe
            found_user = User.query.filter_by(username='test_db_connection').first()
            if found_user:
                print("✅ Usuario verificado en la base de datos")
                # Limpiar usuario de prueba
                db.session.delete(found_user)
                db.session.commit()
                print("✅ Usuario de prueba eliminado")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en la aplicación Flask: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Configurando base de datos para Sistema de Rutas del Ecuador")
    print("=" * 60)
    
    print("\n1. Probando conexión directa a MySQL...")
    mysql_ok = test_mysql_connection()
    
    if mysql_ok:
        print("\n2. Probando conexión desde Flask...")
        app_ok = test_app_connection()
        
        if app_ok:
            print("\n🎉 ¡Configuración exitosa!")
            print("✅ MySQL/MariaDB funcionando correctamente")
            print("✅ Flask puede conectarse y crear tablas")
            print("✅ Las inserciones funcionan correctamente")
            print("\n🚀 Puede ejecutar la aplicación con:")
            print("python app.py")
        else:
            print("\n⚠️  MySQL funciona pero hay problemas con Flask")
            print("💡 Revise la configuración en config.py")
    else:
        print("\n⚠️  MySQL no está disponible")
        print("💡 Opciones:")
        print("   1. Iniciar Laragon y activar MySQL/MariaDB")
        print("   2. La aplicación usará SQLite como fallback")
        print("\n🚀 Puede ejecutar la aplicación de todas formas:")
        print("python app.py")
    
    print("=" * 60)
