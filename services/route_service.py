from services.interfaces import RouteServiceInterface
from services.ecuador_graph import EcuadorCitiesGraph
from models import RouteQuery, db
from sqlalchemy import func

class RouteService(RouteServiceInterface):
    def __init__(self):
        self.graph = EcuadorCitiesGraph()
    
    def calculate_route(self, start_city, end_city):
        """Calcula la ruta más corta entre dos ciudades"""
        return self.graph.calculate_shortest_path(start_city, end_city)
    
    def save_route_query(self, username, start_city, end_city, route, distance):
        """Guarda una consulta de ruta en la base de datos"""
        query = RouteQuery(
            username=username,
            start_city=start_city,
            end_city=end_city,
            total_distance=distance
        )
        query.set_route_from_list(route)
        
        db.session.add(query)
        db.session.commit()
        return query
    
    def get_user_history(self, username):
        """Obtiene el historial de consultas de un usuario"""
        return RouteQuery.query.filter_by(username=username).order_by(
            RouteQuery.query_date.desc()
        ).all()
    
    def get_route_details(self, path):
        """Obtiene detalles de la ruta"""
        return self.graph.get_route_details(path)
    
    def get_provinces(self):
        """Obtiene todas las provincias"""
        return self.graph.get_provinces()
    
    def get_cities_by_province(self, province):
        """Obtiene las ciudades de una provincia"""
        return self.graph.get_cities_by_province(province)
    
    def get_all_cities(self):
        """Obtiene todas las ciudades"""
        return self.graph.get_all_cities()
    
    def get_statistics(self):
        """Obtiene estadísticas del sistema"""
        total_queries = RouteQuery.query.count()
        avg_distance = db.session.query(func.avg(RouteQuery.total_distance)).scalar()
        most_popular_start = db.session.query(
            RouteQuery.start_city, func.count(RouteQuery.start_city)
        ).group_by(RouteQuery.start_city).order_by(
            func.count(RouteQuery.start_city).desc()
        ).first()
        
        most_popular_end = db.session.query(
            RouteQuery.end_city, func.count(RouteQuery.end_city)
        ).group_by(RouteQuery.end_city).order_by(
            func.count(RouteQuery.end_city).desc()
        ).first()
        
        return {
            'total_queries': total_queries,
            'average_distance': round(avg_distance, 2) if avg_distance else 0,
            'most_popular_start': most_popular_start[0] if most_popular_start else 'N/A',
            'most_popular_end': most_popular_end[0] if most_popular_end else 'N/A'
        }
