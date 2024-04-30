"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members


    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    new_member = {
        "id": body['id'],
        "first_name": body['first_name'],
        "age": body['age'],
        "lucky_numbers": body['lucky_numbers']
    }

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.add_member(new_member)
    response_body = {
        "msg": "Done, Member Added"
    }


    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_id(id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    member = next((member for member in members if member['id'] == id), None)
    print(next)

 
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member_id(id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    member = next((member for member in members if member['id'] == id), None)
    
    if member:
        members.remove(member)
        
        response = {
            "done": True
            }
        
        return jsonify(response), 200
    elif member:
        response = {
            "mistake": "Check it again"
            }
        return jsonify(response), 400
    else:
        response = {'error': 'Miembro no encontrado'}
        return jsonify(response), 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
