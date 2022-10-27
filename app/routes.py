from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet

'''
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
'''

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

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = planet_id_validation(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description":planet.description,
        "moons": planet.moons
    }, 200

@planets_bp.route("", methods=['POST'])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name=request_body['name'],
        description=request_body['description'],
        number_moons=request_body['number_moons']
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": f"Successfully created the planet {new_planet.name}"}), 201

@planets_bp.route("",methods=["GET"])
def get_all_planets():
    result =[]
    all_planets = Planet.query.all()
    for planet in all_planets:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description":planet.description,
            "number_moons": planet.number_moons
        }
        result.append(planet_dict)

    return jsonify(result), 200