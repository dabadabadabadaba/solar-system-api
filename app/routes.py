from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet


planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# helper function
def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"message": f"invalid data type:{model_id}"}, 400))

    chosen_object= cls.query.get(model_id)

    if chosen_object is None:
        return abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return chosen_object

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    chosen_planet =get_model_from_id(Planet, planet_id)
    return jsonify(chosen_planet.to_dict()), 200

@planets_bp.route("", methods=['POST'])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": f"Successfully created the planet {new_planet.name}"}), 201

@planets_bp.route("",methods=["GET"])
def get_all_planets():
    name_query_value = request.args.get("name")

    if name_query_value is not None:
        planets = Planet.query.filter_by(name=name_query_value)
    else:
        planets = Planet.query.all()
    
    result =[]
    for planet in planets:
        result.append(planet.to_dict())

    return jsonify(result), 200

@planets_bp.route("/<planet_id>",methods=["PUT"])
def update_one_planet(planet_id):
    update_planet = get_model_from_id(Planet, planet_id)

    request_body = request.get_json() #Changing from Json to python code

    try:
        update_planet.name = request_body['name']
        update_planet.description = request_body['description']
        update_planet.num_of_moons = request_body['num_of_moons']
    except KeyError:
        # refactor this part to give more specific information 
        return jsonify({"msg": "Missing required data"}), 400

    db.session.commit()

    return jsonify({"msg": f"Succesfully updated planet with id # {update_planet.id}"}),200

@planets_bp.route("/<planet_id>",methods=["DELETE"])
def delete_one_planet(planet_id):

    planet_to_delete = get_model_from_id(Planet, planet_id)

    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"msg": f"Succesfully deleted planet with id # {planet_to_delete.id}"}), 200