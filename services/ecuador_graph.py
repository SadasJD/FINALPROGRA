import networkx as nx

class EcuadorCitiesGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.provinces_cities = {
            'Pichincha': ['Quito', 'Cayambe', 'Sangolquí', 'Machachi'],
            'Guayas': ['Guayaquil', 'Milagro', 'Daule', 'Samborondón'],
            'Azuay': ['Cuenca', 'Gualaceo', 'Paute', 'Girón'],
            'Manabí': ['Portoviejo', 'Manta', 'Chone', 'Jipijapa'],
            'Los Ríos': ['Babahoyo', 'Quevedo', 'Ventanas', 'Vinces'],
            'El Oro': ['Machala', 'Pasaje', 'Santa Rosa', 'Arenillas'],
            'Loja': ['Loja', 'Catamayo', 'Cariamanga', 'Macará'],
            'Tungurahua': ['Ambato', 'Baños', 'Pelileo', 'Píllaro'],
            'Imbabura': ['Ibarra', 'Otavalo', 'Cotacachi', 'Atuntaqui'],
            'Cotopaxi': ['Latacunga', 'La Maná', 'Saquisilí', 'Pujilí']
        }
        self._build_graph()
    
    def _build_graph(self):
        """Construye el grafo con todas las conexiones entre ciudades"""
        # Conexiones principales entre provincias (distancias aproximadas en km)
        connections = [
            # Quito como hub principal
            ('Quito', 'Ibarra', 115),
            ('Quito', 'Otavalo', 95),
            ('Quito', 'Latacunga', 89),
            ('Quito', 'Ambato', 135),
            ('Quito', 'Baños', 178),
            ('Quito', 'Cuenca', 465),
            ('Quito', 'Guayaquil', 420),
            ('Quito', 'Portoviejo', 350),
            ('Quito', 'Manta', 380),
            
            # Costa
            ('Guayaquil', 'Portoviejo', 190),
            ('Guayaquil', 'Manta', 220),
            ('Guayaquil', 'Machala', 165),
            ('Guayaquil', 'Babahoyo', 65),
            ('Guayaquil', 'Quevedo', 168),
            ('Guayaquil', 'Milagro', 46),
            ('Guayaquil', 'Daule', 32),
            
            # Manabí
            ('Portoviejo', 'Manta', 35),
            ('Portoviejo', 'Chone', 54),
            ('Portoviejo', 'Jipijapa', 68),
            ('Manta', 'Chone', 78),
            
            # Sierra centro
            ('Latacunga', 'Ambato', 47),
            ('Ambato', 'Baños', 43),
            ('Ambato', 'Riobamba', 52),
            
            # Sierra sur
            ('Cuenca', 'Loja', 210),
            ('Cuenca', 'Gualaceo', 36),
            ('Cuenca', 'Paute', 43),
            ('Loja', 'Catamayo', 36),
            ('Loja', 'Cariamanga', 158),
            ('Loja', 'Macará', 195),
            
            # El Oro
            ('Machala', 'Pasaje', 15),
            ('Machala', 'Santa Rosa', 25),
            ('Machala', 'Arenillas', 56),
            ('Guayaquil', 'Pasaje', 150),
            
            # Los Ríos
            ('Babahoyo', 'Quevedo', 103),
            ('Babahoyo', 'Ventanas', 45),
            ('Babahoyo', 'Vinces', 28),
            ('Quevedo', 'Ventanas', 65),
            ('Quevedo', 'La Maná', 89),
            
            # Imbabura
            ('Ibarra', 'Otavalo', 22),
            ('Ibarra', 'Cotacachi', 15),
            ('Ibarra', 'Atuntaqui', 12),
            ('Otavalo', 'Cotacachi', 18),
            
            # Cotopaxi
            ('Latacunga', 'La Maná', 95),
            ('Latacunga', 'Saquisilí', 25),
            ('Latacunga', 'Pujilí', 32),
            
            # Tungurahua
            ('Ambato', 'Pelileo', 18),
            ('Ambato', 'Píllaro', 22),
            ('Baños', 'Pelileo', 35),
            
            # Azuay interno
            ('Cuenca', 'Girón', 45),
            ('Gualaceo', 'Paute', 15),
            
            # Conexiones adicionales
            ('Cuenca', 'Machala', 195),
            ('Ambato', 'Quevedo', 145),
            ('Latacunga', 'Quevedo', 120),
        ]
        
        # Agregar todas las conexiones al grafo
        for city1, city2, distance in connections:
            self.graph.add_edge(city1, city2, weight=distance)
    
    def get_provinces(self):
        """Retorna la lista de provincias"""
        return list(self.provinces_cities.keys())
    
    def get_cities_by_province(self, province):
        """Retorna las ciudades de una provincia específica"""
        return self.provinces_cities.get(province, [])
    
    def get_all_cities(self):
        """Retorna todas las ciudades disponibles"""
        cities = []
        for province_cities in self.provinces_cities.values():
            cities.extend(province_cities)
        return sorted(cities)
    
    def calculate_shortest_path(self, start_city, end_city):
        """Calcula la ruta más corta entre dos ciudades usando Dijkstra"""
        try:
            path = nx.dijkstra_path(self.graph, start_city, end_city)
            distance = nx.dijkstra_path_length(self.graph, start_city, end_city)
            return path, distance
        except nx.NetworkXNoPath:
            return None, None
        except nx.NodeNotFound:
            return None, None
    
    def get_route_details(self, path):
        """Obtiene detalles de la ruta incluyendo distancias entre ciudades"""
        if not path or len(path) < 2:
            return []
        
        details = []
        total_distance = 0
        
        for i in range(len(path) - 1):
            current_city = path[i]
            next_city = path[i + 1]
            
            if self.graph.has_edge(current_city, next_city):
                distance = self.graph[current_city][next_city]['weight']
                total_distance += distance
                
                details.append({
                    'from': current_city,
                    'to': next_city,
                    'distance': distance,
                    'cumulative_distance': total_distance
                })
        
        return details
