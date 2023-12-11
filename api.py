from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from databas import db, Regions, Parks, Images

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_table.db'
db = SQLAlchemy(api)

# API for search page
# path for dev: localhost/search
# path for deployment: /search
@api.route('localhost/search', methods=['GET'])
def search():
    # get filter parameters
    region = request.args.get('region', default=None, type=str)
    park = request.args.get('park', default=None, type=str)

    # Query database for images
    query = Images.query
    try:
        # filter images by region and park
        if region is not None and park is not None:
            # get selected region
            _region = Regions.query.filter_by(region=region).first()
            if _region:
                # get selected park
                _park = Parks.query.filter_by(park=park).first()
                if _park:
                    # get images associated /w region and park
                    query = query.filter_by(Images.region_id == _region.id, Images.park_id == _park.id)
                else:
                    return make_response(jsonify({'message': 'park not found'}), 404)
            else:
                return make_response(jsonify({'message': 'region not found'}), 404)
            
        # filter images by region
        if region is not None:
            # get selected region
            _region = Regions.query.filter_by(region=region).first()
            if _region:
                # get images associated /w region
                query = query.filter_by(Images.region_id == _region.id)
            else:
                return make_response(jsonify({'message': 'region not found'}), 404)

        
        # Execute query
        _images = Images.query.all() 
        return make_response(jsonify({'images': image.json() for image in _images}), 200)   
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}), 500)