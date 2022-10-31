from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet


planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# helper function
def get_planet_from_id(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return abort(make_response({"message": f"invalid data type:{planet_id}"}, 400))

    chosen_planet= Planet.query.get(planet_id)

    if chosen_planet is None:
        return abort(make_response({"message": f"planet {planet_id} not found"}, 404))
    return chosen_planet

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    chosen_planet =get_planet_from_id(planet_id)
    return jsonify(chosen_planet.to_dict()), 200

@planets_bp.route("", methods=['POST'])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name=request_body['name'],
        description=request_body['description'],
        num_of_moons=request_body['num_of_moons']
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": f"Successfully created the planet {new_planet.name}"}), 201

@planets_bp.route("",methods=["GET"])
def get_all_planets():
    result =[]
    all_planets = Planet.query.all()
    for planet in all_planets:
        result.append(planet.to_dict())

    return jsonify(result), 200