from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from services.user_service import UserService
from services.route_service import RouteService
from datetime import datetime

home_bp = Blueprint('home', __name__)
user_service = UserService()
route_service = RouteService()

@home_bp.route('/')
def home():
    # Si no hay usuario en sesión, mostrar registro
    if 'username' not in session:
        return render_template("home.html", show_registration=True)
    
    # Si hay usuario, mostrar calculadora de rutas 
    # Obtener estadísticas
    stats = route_service.get_statistics()
    
    return render_template("home.html", 
                            show_registration=False,
                            username=session['username'],
                            stats=stats)

@home_bp.route('/register', methods=['POST'])
def register_user():
    # Validación manual 
    username = request.form.get('username', '').strip()
    
    if not username or len(username) < 3:
        flash('El nombre de usuario debe tener al menos 3 caracteres.', 'error')
        return redirect(url_for('home.home'))
    
    if user_service.user_exists(username):
        flash(f'El usuario {username} ya existe. Usando usuario existente.', 'info')
    else:
        user_service.create_user(username)
        flash(f'Usuario {username} registrado exitosamente!', 'success')
        
        session['username'] = username
        return redirect(url_for('home.home'))
    
    flash('Error en el formulario. Verifique los datos.', 'error')
    return redirect(url_for('home.home'))

@home_bp.route('/get_cities/<province>')
def get_cities(province):
    """API endpoint para obtener ciudades de una provincia"""
    cities = route_service.get_cities_by_province(province)
    return jsonify(cities)

@home_bp.route('/calculate_route', methods=['POST'])
def calculate_route():
    if 'username' not in session:
        flash('Debe registrarse primero.', 'error')
        return redirect(url_for('home.home'))
    
    # Obtener datos directamente del request en lugar del formulario WTF
    start_city = request.form.get('start_city')
    end_city = request.form.get('end_city')
    
    # Validaciones básicas
    if not start_city or not end_city:
        flash('Debe seleccionar ciudad de origen y destino.', 'error')
        return redirect(url_for('home.home'))
    
    if start_city == end_city:
        flash('La ciudad de origen y destino no pueden ser iguales.', 'error')
        return redirect(url_for('home.home'))
    
    try:
        # Calcular ruta
        path, distance = route_service.calculate_route(start_city, end_city)
        
        if path is None:
            flash(f'No se encontró una ruta entre {start_city} y {end_city}.', 'error')
            return redirect(url_for('home.home'))
        
        # Guardar consulta
        route_service.save_route_query(
            session['username'], start_city, end_city, path, distance
        )
        
        # Obtener detalles de la ruta
        route_details = route_service.get_route_details(path)
        
        return render_template("route_result.html",
                                start_city=start_city,
                                end_city=end_city,
                                path=path,
                                distance=distance,
                                route_details=route_details,
                                username=session['username'],
                                current_date=datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    except Exception as e:
        flash(f'Error al calcular la ruta: {str(e)}', 'error')
        return redirect(url_for('home.home'))

@home_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('home.home'))

@home_bp.route('/debug')
def debug():
    """Mostrar información de debug"""
    debug_info = {
        'session': dict(session),
        'session_keys': list(session.keys()),
        'username_in_session': 'username' in session,
        'current_username': session.get('username', 'No usuario')
    }
    
    html = "<h1>Debug - Sistema de Rutas</h1>"
    html += f"<p><strong>Usuario en sesión:</strong> {'Sí' if 'username' in session else 'No'}</p>"
    html += f"<p><strong>Username:</strong> {session.get('username', 'No definido')}</p>"
    html += f"<p><strong>Sesión completa:</strong> {dict(session)}</p>"
    html += "<hr>"
    html += '<p><a href="/">Volver al inicio</a></p>'
    html += '<p><a href="/user/test">Probar ruta usuario</a></p>'
    html += '<p><a href="/user/create_test_user">Crear usuario de prueba</a></p>'
    html += '<p><a href="/user/statistics">Ver estadísticas</a></p>'
    
    return html

@home_bp.route('/get_graph_data')
def get_graph_data():
    """API para obtener datos del grafo completo para visualización"""
    try:
        from services.ecuador_graph import EcuadorCitiesGraph
        graph_service = EcuadorCitiesGraph()
        
        # Obtener el grafo de NetworkX
        G = graph_service.graph
        
        # Convertir a formato para Vis.js
        nodes = []
        edges = []
        
        # Crear nodos (ciudades)
        for node in G.nodes():
            nodes.append({
                'id': node,
                'label': node,
                'color': '#97C2FC',
                'font': {'size': 12}
            })
        
        # Crear aristas (conexiones)
        for edge in G.edges(data=True):
            edges.append({
                'from': edge[0],
                'to': edge[1],
                'label': f"{edge[2]['weight']} km",
                'color': '#848484',
                'width': 2
            })
        
        return jsonify({
            'nodes': nodes,
            'edges': edges
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@home_bp.route('/get_route_graph/<start_city>/<end_city>')
def get_route_graph(start_city, end_city):
    """API para obtener visualización del grafo con ruta específica resaltada"""
    try:
        from services.ecuador_graph import EcuadorCitiesGraph
        graph_service = EcuadorCitiesGraph()
        
        # Calcular la ruta
        path, distance = graph_service.calculate_shortest_path(start_city, end_city)
        
        if not path:
            return jsonify({'error': 'No se encontró ruta'}), 404
        
        # Obtener el grafo completo
        G = graph_service.graph
        
        # Convertir a formato para Vis.js
        nodes = []
        edges = []
        
        # Crear nodos
        for node in G.nodes():
            color = '#FF6B6B' if node in path else '#97C2FC'  # Rojo para ruta, azul para otros
            size = 25 if node in path else 20
            
            nodes.append({
                'id': node,
                'label': node,
                'color': color,
                'size': size,
                'font': {'size': 14 if node in path else 12}
            })
        
        # Crear aristas
        for edge in G.edges(data=True):
            # Verificar si esta arista está en la ruta
            is_in_route = False
            for i in range(len(path) - 1):
                if  (edge[0] == path[i] and edge[1] == path[i+1]) or \
                    (edge[1] == path[i] and edge[0] == path[i+1]):
                    is_in_route = True
                    break
            
            color = '#FF6B6B' if is_in_route else '#848484'  # Rojo para ruta, gris para otros
            width = 4 if is_in_route else 2
            
            edges.append({
                'from': edge[0],
                'to': edge[1],
                'label': f"{edge[2]['weight']} km",
                'color': color,
                'width': width
            })
        
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'path': path,
            'distance': distance
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
