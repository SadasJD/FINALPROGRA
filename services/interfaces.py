from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    def create_user(self, username):
        pass
    
    @abstractmethod
    def get_user(self, username):
        pass
    
    @abstractmethod
    def user_exists(self, username):
        pass

class RouteServiceInterface(ABC):
    @abstractmethod
    def calculate_route(self, start_city, end_city):
        pass
    
    @abstractmethod
    def save_route_query(self, username, start_city, end_city, route, distance):
        pass
    
    @abstractmethod
    def get_user_history(self, username):
        pass
