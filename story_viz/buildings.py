import random
import numpy as np
from interests import *
import importlib

# Takes a dictionary specifying {building_class : num_buildings}
def building_generator(building_spec):
    buildings = []
    building_id = 0
    for building_class_name, num_buildings in building_spec.items():
        for _ in range(num_buildings):
            # Load "module.submodule.MyClass"
            BuildingClass = getattr(importlib.import_module("buildings"), building_class_name)
            # Instantiate the class (pass arguments to the constructor, if needed)
            buildings.append(BuildingClass(building_id))
            building_id += 1
    return buildings

def normalize_vector(vector, only_greater_than=False):
    distance = np.linalg.norm(vector)
    if distance != 0:
        if not only_greater_than or distance > 1:
            return vector / distance
    return vector

class Building(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.building_type = ""
        self.position = np.array([0,0])
        self.dim = np.array([0,0])
        self.social_agents = []
        self.knn = 0
        self.attraction = np.inf
        self.repulsion = -1

    def set_position(self, position, z, x):
        new_z = position[0]
        if position[0] < 0:
            new_z = 0
        elif position[0] + max(self.dim) > z-1:
            new_z = z-1 - max(self.dim)

        new_x = position[1]
        if position[1] < 0:
            new_x = 0
        elif position[1] + max(self.dim) > x-1:
            new_x = x-1 - max(self.dim)

        self.position = np.round([new_z, new_x]).astype(int)

    def get_interest(self, village_skeleton, terrain):
        return np.array([0,0])


class Rural(Building):
    def __init__(self, id, type):
        super(Rural, self).__init__(id, type)
        self.building_type = "rural"


class Residential(Building):
    def __init__(self, id, type):
        super(Residential, self).__init__(id, type)
        self.building_type = "residential"


class Commercial(Building):
    def __init__(self, id, type):
        super(Commercial, self).__init__(id, type)
        self.building_type = "commercial"


class Public(Building):
    def __init__(self, id, type):
        super(Public, self).__init__(id, type)
        self.building_type = "public"


class Aesthetic(Building):
    def __init__(self, id, type):
        super(Aesthetic, self).__init__(id, type)
        self.building_type = "aesthetic"



class House(Residential):
    def __init__(self, id):
        super(House, self).__init__(id, "house")
        self.dim = np.array([7,10])
        self.social_agents = ["house"]
        self.knn = 10
        self.attraction = 40
        self.repulsion = 10

    def get_interest(self, village_skeleton, terrain):
        social_vector = sociability(terrain, village_skeleton, self)
        slope_vector = slope(terrain, village_skeleton, self)

        return normalize_vector(social_vector, True) * 5 + normalize_vector(slope_vector, True) * 2

    def get_noise(self, scale=1):
        noise_vector = np.array([random.uniform(-1,1), random.uniform(-1,1)])
        noise_vector = noise_vector / np.linalg.norm(noise_vector)
        return noise_vector * scale

class Farm(Rural):
    def __init__(self, id):
        super(Farm, self).__init__(id, "farm")
        self.dim = np.array([10,10])
        self.social_agents = ["farm"]
        self.knn = 4
        self.attraction = 20
        self.repulsion = 10

    def get_interest(self, village_skeleton, terrain):
        social_vector = sociability(terrain, village_skeleton, self)
        slope_vector = slope(terrain, village_skeleton, self)
        return normalize_vector(social_vector, True) * 2 + normalize_vector(slope_vector, True) * 2

class Church(Public):
    def __init__(self, id):
        super(Church, self).__init__(id, "church")
        self.dim = np.array([40,40])
        self.influence_radius = 100

    def get_interest(self, village_skeleton, terrain):
        domination_vector = geographic_domination(terrain, village_skeleton, self)
        return normalize_vector(domination_vector, True) * 2


