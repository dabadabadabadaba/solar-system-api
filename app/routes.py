from time import monotonic_ns
from flask import Blueprint, jsonify, abort, make_response

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

def planet_id_validation(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"message": f"invalid data type:{planet_id}"}, 400))

    for planet in planets:
        if planet.id ==planet_id:
            return planet
    abort(make_response({"message": f"planet {planet_id} not found"}, 404))


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

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = planet_id_validation(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description":planet.description,
        "moons": planet.moons
    }, 200



