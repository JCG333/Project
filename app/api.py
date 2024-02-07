'''
====== TABLE OF CONTENTS ======
1. Import Statements
2. Create Tables
    - create_tables(): create tables if they don't exist
2. Routes
    - /: index:
    - /login: login user
    - /logout: logout user
    - /register: register user
    - /search: search for images based on the filter parameters
    - /company: get the company id
    - /region: get the region id
    - /park: get the park id
    - /create: create a new entry in the database
    - /regions: get all regions
    - /parks: get all parks
    - /search_turbine/<search_term>: search for turbines based on the search term
    - /search_page: get the search page
    - /account: get the account page
    - /turbine/<turbineId>: get the turbine page

'''
import os
from flask import *
from flask_login import *
from os import environ, urandom
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

# define an app instance
api = Flask(__name__)

# get the db url from the environment variable
api.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'
api.config["SECRET_KEY"] = urandom(20)  # TEST

# import the db instance and the models
from db.schema import db, Users, Companies, Regions, Parks, Turbines, ImageUrl

login_manager = LoginManager()
login_manager.init_app(api)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def load_users():
    if current_user.is_authenticated:
        return current_user.username
    else:
        return "Guest"


'''----- create tables if they don't exist -----'''


def create_tables():
    print("create_tables function called")
    with api.app_context():
        db.init_app(api)
        db.create_all()

        # DEVELOPMENT ONLY

        try:
            # Add default entries
            default_company = Companies(company='Company1')
            db.session.add(default_company)
            db.session.commit()
            default_region = Regions(region='Region1', company_id=default_company.id)
            db.session.add(default_region)
            db.session.commit()
            default_park = Parks(park='Park1', region_id=default_region.id, company_id=default_company.id)
            db.session.add(default_park)
            default_park2 = Parks(park='Park2', region_id=default_region, company_id=default_company)
            db.session.add(default_park2)
            db.session.commit()
            default_Turbine = Turbines(turbine='Turbine1', company_id=default_company.id, region_id=default_region.id,
                                       park_id=default_park.id)
            db.session.add(default_Turbine)
            default_Turbine2 = Turbines(turbine='Turbine2', company_id=default_company, region_id=default_region,
                                        park_id=default_park2.id)
            db.session.add(default_Turbine2)
            db.session.commit()
            default_image = ImageUrl(image_url='https://www.google.com', weather_data='Sunny', date_time=datetime.now(),
                                     turbine_id=default_Turbine.id)
            db.session.add(default_image)
            default_image2 = ImageUrl(image_url='https://www.Microsoft.com', weather_data='Cloudy',
                                      date_time=datetime.now(), turbine_id=default_Turbine2.id)
            db.session.add(default_image2)
            db.session.commit()

            print('Default entries added successfully')
        except Exception as e:
            print('Failed to add default entries, error: ', e)


create_tables()

'''
================== ROUTES ==================
'''

'''----- API Health check -----'''


@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200


@api.route('/')
# @login_required OM MAN VILL GÖRA SÅ MAN INTE KOMMER IN UTAN INLOGGNING
def home():
    data = {
        'title': 'Service for snow and ice detection',
        'header': 'Service for snow and ice detection',
        'welcome_message': 'Welcome to the service for snow and ice detection!',
        'user': load_users(),
        'content': 'Contents',
        'footer_text': 'Service for snow and ice detection. All rights reserved.'
    }
    return render_template('index.html', **data)


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        user = Users(username=username, password=hashed_password, privilege="0")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@api.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@api.route("/turbine")
def turbine():
    return render_template("turbinePage.html")


'''----- Search page route -----'''


@api.route('/search', methods=['POST'])
def search():
    # get filter parameters body
    filters = request.get_json()
    region_name = filters.get('region')
    park_name = filters.get('park')
    company_name = filters.get('company')
    print('region_name: ', region_name)
    print('park_name: ', park_name)
    print('company_name: ', company_name)

    # get ids for each filter
    try:
        if region_name != ' ':
            region_id = Regions.query.filter_by(region=region_name).first().id
        if park_name != ' ':
            park_id = Parks.query.filter_by(park=park_name).first().id
        if company_name != ' ':
            company_id = Companies.query.filter_by(company=company_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting ids', 'error': str(e)}), 500)

    try:
        # Query database for image
        if region_name != ' ' and park_name != ' ':
            # filter images by region and park
            query = Turbines.query.filter_by(region_id=region_id, park_id=park_id, company_id=company_id)
        elif region_name != ' ':
            # filter images by region
            query = Turbines.query.filter_by(region_id=region_id, company_id=company_id)
        elif park_name != ' ':
            # filter images by park
            query = Turbines.query.filter_by(park_id=park_id, company_id=company_id)
        else:
            # no filter
            query = Turbines.query.filter_by(company_id=company_id)

        # get all images that match the specified critera
        query = query.all()
    except Exception as e:
        return make_response(jsonify({'message': 'error getting turbine(s)', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'turbines': [turbine.json() for turbine in query]}), 200)


'''----- Get company id -----'''


@api.route('/company', methods=['POST'])
def get_company_id():
    # get company name from body
    company_name = request.get_json().get('company')

    try:
        # Query database for company id
        company_id = Companies.query.filter_by(company=company_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting company id', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'company_id': company_id}), 200)


'''----- Get region id -----'''


@api.route('/region', methods=['POST'])
def get_region_id():
    # get region name from body
    region_name = request.get_json().get('region')

    try:
        # Query database for region id
        region_id = Regions.query.filter_by(region=region_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting region id', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'region_id': region_id}), 200)


'''----- Get park id ----- '''


@api.route('/park', methods=['POST'])
def get_park_id():
    # get park name from body
    park_name = request.get_json().get('park')

    try:
        # Query database for park id
        park_id = Parks.query.filter_by(park=park_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting park id', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'park_id': park_id}), 200)


'''----- Create a new turbine ----- '''


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


'''----- Get regions -----'''


@api.route('/regions', methods=['GET'])
def regions():
    try:
        # Query database for regions
        regions = Regions.query.all()
    except Exception as e:
        return make_response(jsonify({'message': 'error getting regions', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'regions': [region.json() for region in regions]}), 200)


'''----- Get parks -----'''


@api.route('/parks', methods=['GET'])
def parks():
    try:
        # Query database for parks
        parks = Parks.query.all()
    except Exception as e:
        return make_response(jsonify({'message': 'error getting parks', 'error': str(e)}), 500)

        # get all images that match the specified critera
    return make_response(jsonify({'parks': [park.json() for park in parks]}), 200)


'''----- search using turbine name----- '''


@api.route('/search_turbine/<search_term>', methods=['GET'])
def search_turbine(search_term):
    try:
        turbines = Turbines.query.filter(Turbines.turbine.ilike('%' + search_term + '%')).all()
        return make_response(jsonify({'turbines': [turbine.json() for turbine in turbines]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error searching for turbines', 'error': str(e)}), 500)


'''
=================== PAGES ===================
'''

'''----- Get Search page -----'''


@api.route('/search_page', methods=['GET'])
def search_page():
    return render_template('search.html')


'''----- Get Account page -----'''


@api.route('/account', methods=['GET'])
def account_page():
    return render_template('account.html')


'''----- Get turbine page -----'''


@api.route('/turbine/<turbineId>', methods=['GET'])
def turbine_page(turbineId):
    return render_template('turbine.html', turbineId=turbineId)


@api.route('/help-support', methods=['GET'])
def help_support():
    return render_template('help-support.html')


try:
    # Your existing code to start the Flask application
    logging.info('Starting application...')
    api.run(host='0.0.0.0', port=4000, debug=True)
except Exception as e:
    logging.exception('Failed to start application')
