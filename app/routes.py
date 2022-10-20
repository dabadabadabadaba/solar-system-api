from time import monotonic_ns
from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons


planets = [
    Planet(1, "Mars", "the Red Planet", ["Deimos", "Phobos"]),
    Planet(2, "Mercury", "the smallest planet", []),
    Planet(3, "Earth", "home", ["Moon"])
    ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("",methods=["GET"])
def get_all_planets():
    result =[]
    for planet in planets:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description":planet.description,
            "moons": planet.moons
        }
        result.append(planet_dict)

    return jsonify(result), 200


