import json
from math import pi
import matplotlib as plt

class Agent:
    def __init__(self,position, **agent_attributes):
        self.position = position
        for key, value in agent_attributes.items():
            setattr(self, key, value)

class Position:
    def __init__(self, longitude_degrees, latitude_degrees):
        self.latitude_degrees = latitude_degrees
        self.longitude_degrees = longitude_degrees

    @property
    def longitude(self):
        return self.longitude_degrees * pi /180

    @property
    def latitude(self):
        return self.latitude_degrees * pi /180

class Zone:
    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1
    HEIGHT_DEGREES = 1
    ZONES = []
    EARTH_RADIUS_KILOMETERS = 6371

    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self.inhabitants = []

    @classmethod
    def _initialize_zone(cls):
        for latitude in range(cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)

    def contains(self, position):
        return position.longitude >= min(self.corner1.longitude, self.corner2.longitude) and \
               position.longitude < max(self.corner1.longitude, self.corner2.longitude) and \
               position.latitude >= min(self.corner1.latitude, self.corner2.latitude) and \
               position.latitude < max(self.corner1.latitude, self.corner2.latitude)

    @classmethod
    def find_zone_that_contains(cls, position):
        if not cls.ZONES:
            cls._initialize_zone()
        # Compute the index in the ZONES array that contains the given position
        longitude_index = int((position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        latitude_index = int((position.latitude_degrees - cls.MIN_LATITUDE_DEGREES) / cls.HEIGHT_DEGREES)
        longitude_bins = int((cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)  # 180-(-180) / 1
        zone_index = latitude_index * longitude_bins + longitude_index

        # Just checking that the index is correct
        zone = cls.ZONES[zone_index]
        assert zone.contains(position)
        return zone

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    @property
    def population(self):
        return len(self.inhabitants)

    @property
    def width(self):
        return abs((self.corner1.longitude - self.corner2.longitude)) * self.EARTH_RADIUS_KILOMETERS

    @property
    def height(self):
        return abs(self.corner1.latitude - self.corner2.latitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def area(self):
        return self.height * self.width

    def population_density(self):
        return self.population / self.area

    def average_agreeableness(self):
        if not self.inhabitants:
            return 0
        return sum([inhabitant.agreeableness for inhabitant in self.inhabitants]) / self.population

class BaseGraph:

    def __init__(self):
        self.title = "Your graph title"
        self.x_label = "X-axis label"
        self.y_label = "X-axis label"
        self.show_grid = True

    def show(self, zones):
        # x_values = gather only x_values from our zones
        # y_values = gather only y_values from our zones
        plt.plot(x_values, y_values, '.')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.show_grid)
        plt.show()

    def xy_values(self, zones):
        raise NotImplementedError
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values
class AgreeablenessGraph(BaseGraph):

    def __init__(self):
        super().__init__()
        self.title = "Nice people live in the countryside"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values

def main():
    for agent_attributes in json.load((open("agents-100k.json"))):
        latitude = agent_attributes.pop("latitude")
        longitude = agent_attributes.pop("longitude")
        position = Position(longitude, latitude)
        agent = Agent(position, **agent_attributes)
        zone = Zone.find_zone_that_contains(position)
        zone.add_inhabitant(agent)
        # Initialisation du graphique
        # agreeableness_graph = AgreeablenessGraph()

        # Affichage du graphique. On passe en paramètre la liste de nos zones pour y avoir accès à l'intérieur de notre classe AgreeablenessGraph.
        # agreeableness_graph.show(Zone.ZONES)
        #print(zone.average_agreeableness())
        #print(agent.position.longitude, agent.position.latitude, sep=' --- ')


main()