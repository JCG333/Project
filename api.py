from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from databas import db, User, Region, Park

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_table.db'
db = SQLAlchemy(api)

@api.route('home/upload/data', methods=['GET'])
def get_image():
    try:
        _input = request.get_json()
        _region = Region.query.filter_by(region=_input['region']).first()
        _linked_park = _region.linked_parks #foreign key
        _park = _input['park']
        _parks = Park.query.filter_by(linked_parks=_linked_park, park=_park).all()
                
        
        selected_park = Park.query.filter_by(park=_park)
        _image = User.query.filter_by(date=_input['date']).first()
        if _input:
            return make_response(jsonify({'users': _input.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}), 500)