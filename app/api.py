'''
Filename: api.py

This is the API for the application. It contains the routes that will be used to
access the database. The routes are:
    - /search (POST)
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

from db.schema import db, Companies, Regions, Parks, Turbines, ImageUrl 

# create tables if they don't exist
def create_tables():
    print("create_tables function called")
    with api.app_context():
        db.init_app(api)
        db.create_all()

        #====== DEVELOPMENT ONLY ======#

        try:
            # Add default entries
            '''
            default_company = Companies(company = 'Company1')
            db.session.add(default_company)
            db.session.commit()
            default_region = Regions(region = 'Region1', company_id = default_company.id)
            db.session.add(default_region)
            db.session.commit()
            default_park = Parks(park = 'Park1', region_id = default_region.id, company_id = default_company.id)
            db.session.add(default_park)
            default_park2 = Parks(park = 'Park2', region_id = default_region, company_id = default_company)
            db.session.add(default_park2)
            db.session.commit()
            default_Turbine = Turbines(turbine = 'Turbine1', company_id = default_company.id, region_id = default_region.id, park_id = default_park.id)
            db.session.add(default_Turbine)
            default_Turbine2 = Turbines(turbine = 'Turbine2', company_id = default_company, region_id = default_region, park_id = default_park2.id)
            db.session.add(default_Turbine2)
            db.session.commit()
            default_image = ImageUrl(image_url = 'https://www.google.com', weather_data = 'Sunny', date_time = datetime.now(), turbine_id = default_Turbine.id)
            db.session.add(default_image)
            default_image2 = ImageUrl(image_url = 'https://www.Microsoft.com', weather_data = 'Cloudy', date_time = datetime.now(), turbine_id = default_Turbine2.id)
            db.session.add(default_image2)
            db.session.commit()
            '''

            print('Default entries added successfully')
        except Exception as e:
            print('Failed to add default entries, error: ', e)

        #==============================#

create_tables() 

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'success'}), 200


'''================== ROUTES =================='''     
# Search page route
@api.route('/search', methods=['POST'])
def search():
    # get filter parameters body
    filters = request.get_json()
    region_name = filters.get('region')
    park_name = filters.get('park')
    company_name = filters.get('company')

    # get ids for each filter
    try:
        if region_name is not None:
            region_id = Regions.query.filter_by(region = region_name).first().id
        if park_name is not None:
            park_id = Parks.query.filter_by(park = park_name).first().id
        if company_name is not None:
            company_id = Companies.query.filter_by(company = company_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting ids', 'error': str(e)}), 500)

    try:
        # Query database for image
        if region_name is not None and park_name is not None:
            # filter images by region and park
            query = Turbines.query.filter_by(region_id = region_id, park_id = park_id, company_id = company_id)
        elif region_name is not None and park_name is None:
            # filter images by region
            query = Turbines.query.filter_by(region_id = region_id, company_id = company_id)
        elif region_name is None and park_name is not None:
            # filter images by park
            query = Turbines.query.filter_by(park_id = park_id, company_id = company_id)
        else:   
            # no filter
            query = Turbines.query.filter_by(company_id = company_id)

        # get all images that match the specified critera
        query = query.all()
    except Exception as e:
        return make_response(jsonify({'message': 'error getting turbine(s)', 'error': str(e)}), 500)  
      
    # get all images that match the specified critera
    return make_response(jsonify({'turbines': [turbine.json() for turbine in query]}), 200)


# Get company id 
@api.route('/company', methods=['POST'])
def get_company_id():
    # get company name from body
    company_name = request.get_json().get('company')

    try:
        # Query database for company id
        company_id = Companies.query.filter_by(company = company_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting company id', 'error': str(e)}), 500)  
      
    # get all images that match the specified critera
    return make_response(jsonify({'company_id': company_id}), 200)

# Get region id
@api.route('/region', methods=['POST'])
def get_region_id():
    # get region name from body
    region_name = request.get_json().get('region')

    try:
        # Query database for region id
        region_id = Regions.query.filter_by(region = region_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting region id', 'error': str(e)}), 500)  
      
    # get all images that match the specified critera
    return make_response(jsonify({'region_id': region_id}), 200)

# Get park id
@api.route('/park', methods=['POST'])
def get_park_id():
    # get park name from body
    park_name = request.get_json().get('park')

    try:
        # Query database for park id
        park_id = Parks.query.filter_by(park = park_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting park id', 'error': str(e)}), 500)  
      
    # get all images that match the specified critera
    return make_response(jsonify({'park_id': park_id}), 200)

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