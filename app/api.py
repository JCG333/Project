'''
Filename: api.py

This is the API for the application. It contains the routes that will be used to
access the database. The routes are:
    - /search (GET)
    - /create (POST)
    -
'''
import os
from flask import Flask, request, jsonify, make_response
from os import environ
from datetime import datetime

# create an app instance
api = Flask(__name__) 

# get the db url from the environment variable
api.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 

from db.schema import images, db 

# create tables if they don't exist
def create_tables():
    with api.app_context():
        db.init_app(api)
        db.create_all()

        #====== DEVELOPMENT ONLY ======#

        # Add default entries
        default_image1 = images(date=datetime.now(), url='http://example.com/image1.jpg', company='Company1', region='Region1', park='Park1', turbine='Turbine1')
        default_image2 = images(date=datetime.now(), url='http://example.com/image2.jpg', company='Company2', region='Region2', park='Park2', turbine='Turbine2')
        default_image3 = images(date=datetime.now(), url='http://example.com/image3.jpg', company='Company1', region='Region3', park='Park3', turbine='Turbine3')
        default_image4 = images(date=datetime.now(), url='http://example.com/image4.jpg', company='Company2', region='Region1', park='Park1', turbine='Turbine4')

        db.session.add(default_image1)
        db.session.add(default_image2)
        db.session.add(default_image3)
        db.session.add(default_image4)

        db.session.commit()

        #==============================#

create_tables() 

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'success'}), 200


'''================== ROUTES =================='''
# Search page route
@api.route('/search', methods=['GET'])
def search():
    # get filter parameters body
    filters = request.get_json()
    region = filters.get('region')
    park = filters.get('park')

    # Query database for image
    query = images.query
    try:
        # filter images by region
        if region is not None and park is None:
            query = query.filter_by(region = region)
        # filter images by park
        elif region is None and park is not None:
            query = query.filter_by(park = park)
        # filter images by region and park
        elif region is not None and park is not None:
            query = query.filter_by(region = region, park = park)
        # no filter
        else:
            pass
        
        # get all images that match the specified critera
        _images = query.all() 
        return make_response(jsonify({'images': [image.json() for image in _images]}), 200)   
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)
     

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
    

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=4000)