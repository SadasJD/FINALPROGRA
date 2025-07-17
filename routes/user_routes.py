from flask import Blueprint, render_template, session, redirect, url_for, flash
from services.user_service import UserService
from services.route_service import RouteService

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_service = UserService()
route_service = RouteService()

@user_bp.route('/test')
def test():
    """Ruta de prueba"""
    return "<h1>Ruta de usuario funcionando</h1>"

@user_bp.route('/history')
def history():
    """Muestra el historial de consultas del usuario actual"""
    try:
        if 'username' not in session:
            flash('Debe registrarse primero.', 'error')
            return redirect(url_for('home.home'))
        
        username = session['username']
        queries = route_service.get_user_history(username)
        
        return render_template("user/history.html", 
                            queries=queries, 
                            username=username)
    except Exception as e:
        return f"<h1>Error al cargar historial</h1><p>{str(e)}</p><a href='/'>Volver</a>"

@user_bp.route('/statistics')
def statistics():
    """Muestra estadísticas generales del sistema"""
    try:
        stats = route_service.get_statistics()
        all_users = user_service.get_all_users()
        
        return render_template("user/statistics.html", 
                                stats=stats,
                                total_users=len(all_users))
    except Exception as e:
        return f"<h1>Error al cargar estadísticas</h1><p>{str(e)}</p><a href='/'>Volver</a>"

@user_bp.route('/create_test_user')
def create_test_user():
    """Crear usuario de prueba para testing"""
    try:
        from flask import session
        test_user = user_service.create_user('test_user_demo')
        session['username'] = 'test_user_demo'
        return redirect(url_for('user.history'))
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"
