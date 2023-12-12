import os
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from db.databas import db, Regions, Parks, Images

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_table.db'
db = SQLAlchemy(api)

# API for search page
# path for dev: localhost/search
# path for deployment: /search
@api.route('/search', methods=['GET'])
def search():
    # get filter parameters
    region = request.args.get('region', default=None, type=str)
    park = request.args.get('park', default=None, type=str)
    turbine = request.args.get('turbine', default=None, type=str)

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

        image_id = request.args.get('image_id', default=None, type=int)
        if image_id is not None:
            # Retrieve image by ID
            image = Images.query.get(image_id)
            if image:
                return make_response(jsonify({'image': image.json()}), 200)
            else:
                return make_response(jsonify({'message': 'image not found'}), 404)
        
        # Execute query
        _images = Images.query.all() 
        return make_response(jsonify({'images': image.json() for image in _images}), 200)   
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}), 500)
    

UPLOAD_FOLDER = '/home/upload/data'
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

@api.route('/create', methods=['POST'])
def create():
    try:
        # Get parameters from the request
        region = request.form.get('region')
        company = request.form.get('company')
        park = request.form.get('park')
        turbine = request.form.get('turbine')

        # Check if all parameters are provided
        if None in (region, company, park, turbine):
            return make_response(jsonify({'message': 'Missing parameters'}), 400)

        # Check if the 'file' key is in the request.files dictionary
        if 'file' not in request.files:
            return make_response(jsonify({'message': 'No file part'}), 400)

        # Get the file from the request
        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return make_response(jsonify({'message': 'No selected file'}), 400)

        # Construct the folder structure
        folder_path = os.path.join(api.config['UPLOAD_FOLDER'], company, region, park, turbine)

        # Construct the file path
        file_path = os.path.join(folder_path, file.filename)

        # Save the file
        file.save(file_path)

        return make_response(jsonify({'message': 'File uploaded successfully'}), 200)

    except Exception as e:
        return make_response(jsonify({'message': 'Error uploading file'}), 500)

