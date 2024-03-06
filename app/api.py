'''
====== TABLE OF CONTENTS ======
1. Import Statements
2. Create Tables
    - create_tables(): create tables if they don't exist
2. Routes
    - !MAINTENENCE
        - /health: API Health check
    - TURBINES
        - /search: Search page route
        - /create: Create a new turbine
        - /search_turbine/<search_term>: search using turbine name
        - /get_pinned: get pinned turbines
        - /pin_turbine/<turbine_id>: pin turbine
        - /unpin_turbine/<turbine_id>: unpin turbine
    - LOCATIONS
        - /company: Get company id
        - /region: Get region id
        - /park: Get park id
        - /regions: Get regions
        - /parks: Get parks
    - USER
        - /change_password: Change password
        - /: Index/login route
        - /logout: Logout route
        - /register: Register page
    - PAGES
        - /turbine: Get Turbine page
        - /search_page: Get Search page
        - /account: Get Account page
        - /turbine/<turbineId>: Get turbine page
        - /help-support: Get help and support page
3. Run the application
    - try: Start the Flask application

    Use (!) to find the different sections

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
api.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
api.config["SECRET_KEY"] = urandom(20)  # TEST

# import the db instance and the models
from db.schema import db, Companies, Regions, Parks, Turbines, ImageUrl, PinnedTurbines, Users, PinnedTurbines, WeatherData

login_manager = LoginManager()
login_manager.init_app(api)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
login_manager.login_view = "login"

def load_users():
    if current_user.is_authenticated:
        return current_user.email
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

            default_company2 = Companies(company='Company2')
            db.session.add(default_company2)
            db.session.commit()

            default_region = Regions(region='Region1', company_id=default_company.id)
            db.session.add(default_region)
            db.session.commit()

            default_park = Parks(park='Park1', company_id=default_company.id, region_id=default_region.id, coordinates='63.408902,16.168218')
            db.session.add(default_park)
            db.session.commit()

            default_park2 = Parks(park='Park2', company_id=default_company.id, region_id=default_region.id, coordinates='63.408902,16.168218')
            db.session.add(default_park2)
            db.session.commit()

            default_turbine = Turbines(turbine='Turbine1', company_id=default_company.id, region_id=default_region.id, park_id=default_park.id)
            db.session.add(default_turbine)
            db.session.commit()

            default_turbine2 = Turbines(turbine='Turbine2', company_id=default_company.id, region_id=default_region.id, park_id=default_park2.id)
            db.session.add(default_turbine2)
            db.session.commit()

            for i in range(3, 20):
                default_turbine = Turbines(turbine=f'Turbine{i}', company_id=default_company.id, region_id=default_region.id, park_id=default_park.id)
                db.session.add(default_turbine)
                db.session.commit()

            default_weather_data = WeatherData(validtime='2022-01-01T00:00:00', date_hour='2022-01-01T00:00:00', request_coordinates='0,0', fetched_coordinates='0,0', msl=1013.0, t=20.0, vis=10.0, wd=180, ws=5.0, r=0, tstm=0, tcc_mean=0, lcc_mean=0, mcc_mean=0, hcc_mean=0, gust=5.0, pmin=1013.0, pmax=1013.0, spp=0, pcat=0, pmean=0.0, pmedian=0.0, Wsymb2=0, park_id=default_park.id)
            db.session.add(default_weather_data)
            db.session.commit()

            default_weather_data2 = WeatherData(validtime='2022-01-02T00:00:00', date_hour='2022-01-02T00:00:00', request_coordinates='0,0', fetched_coordinates='0,0', msl=1014.0, t=21.0, vis=11.0, wd=181, ws=6.0, r=1, tstm=1, tcc_mean=1, lcc_mean=1, mcc_mean=1, hcc_mean=1, gust=6.0, pmin=1014.0, pmax=1014.0, spp=1, pcat=1, pmean=1.0, pmedian=1.0, Wsymb2=1, park_id=default_park.id)
            db.session.add(default_weather_data2)
            db.session.commit()

            default_weather_data3 = WeatherData(validtime='2022-01-03T00:00:00', date_hour='2022-01-03T00:00:00', request_coordinates='0,0', fetched_coordinates='0,0', msl=1015.0, t=22.0, vis=12.0, wd=182, ws=7.0, r=2, tstm=2, tcc_mean=2, lcc_mean=2, mcc_mean=2, hcc_mean=2, gust=7.0, pmin=1015.0, pmax=1015.0, spp=2, pcat=2, pmean=2.0, pmedian=2.0, Wsymb2=2, park_id=default_park.id)
            db.session.add(default_weather_data3)
            db.session.commit()

            default_weather_data4 = WeatherData(validtime='2022-01-04T00:00:00', date_hour='2022-01-04T00:00:00', request_coordinates='0,0', fetched_coordinates='0,0', msl=1016.0, t=23.0, vis=13.0, wd=183, ws=8.0, r=3, tstm=3, tcc_mean=3, lcc_mean=3, mcc_mean=3, hcc_mean=3, gust=8.0, pmin=1016.0, pmax=1016.0, spp=3, pcat=3, pmean=3.0, pmedian=3.0, Wsymb2=3, park_id=default_park.id)
            db.session.add(default_weather_data4)
            db.session.commit()

            default_weather_data5 = WeatherData(validtime='2022-01-05T00:00:00', date_hour='2022-01-05T00:00:00', request_coordinates='0,0', fetched_coordinates='0,0', msl=1017.0, t=24.0, vis=14.0, wd=184, ws=9.0, r=4, tstm=4, tcc_mean=4, lcc_mean=4, mcc_mean=4, hcc_mean=4, gust=9.0, pmin=1017.0, pmax=1017.0, spp=4, pcat=4, pmean=4.0, pmedian=4.0, Wsymb2=4, park_id=default_park.id)
            db.session.add(default_weather_data5)
            db.session.commit()

            default_image = ImageUrl(datetime=str(datetime.now()), date_hour=str(datetime.now().hour), camera1_url='https://www.google.com', camera2_url='https://www.Microsoft.com', turbine_id=default_turbine.id, weather_id=default_weather_data.id)
            db.session.add(default_image)
            db.session.commit()

            default_image2 = ImageUrl(datetime=str(datetime.now()), date_hour=str(datetime.now().hour), camera1_url='https://www.Microsoft.com', camera2_url='https://www.google.com', turbine_id=default_turbine2.id, weather_id=default_weather_data.id)
            db.session.add(default_image2)
            db.session.commit()

            password = generate_password_hash('password')
            default_user = Users(email='user1@gmail.com', password=password, privilege=1, company_id=default_company.id)
            db.session.add(default_user)
            db.session.commit()

            default_pinned_turbine = PinnedTurbines(turbine_id=default_turbine.id, user_id=1)
            db.session.add(default_pinned_turbine)
            db.session.commit()

            for i in range(2, 10):
                default_pinned_turbine = PinnedTurbines(turbine_id=i, user_id=1)
                db.session.add(default_pinned_turbine)
                db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")

create_tables() 

'''
================== !ROUTES ==================
'''

'''
================== !MAINTENENCE ==================
'''

'''----- API Health check -----'''
@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

'''
================== !TURBINES ==================
'''

'''----- Search page route -----'''
@api.route('/search', methods=['POST'])
@login_required
def search():
    # get filter parameters body
    filters = request.get_json()
    region_name = filters.get('region')
    park_name = filters.get('park')
    if current_user.company_id == None:
        return make_response(jsonify({'message': 'not assigned to a company'}), 500)
    company_name = Companies.query.filter_by(id=current_user.company_id).first().company

    # get ids for each filter
    try:
        if region_name != ' ':
            region_id = Regions.query.filter_by(region = region_name).first().id
        if park_name != ' ':
            park_id = Parks.query.filter_by(park = park_name).first().id
        if company_name != ' ':
            company_id = Companies.query.filter_by(company = company_name).first().id
    except Exception as e:
        return make_response(jsonify({'message': 'error getting ids', 'error': str(e)}), 500)

    try:
        # Query database for image
        if region_name != ' ' and park_name != ' ':
            # filter images by region and park
            query = Turbines.query.filter_by(region_id = region_id, park_id = park_id, company_id = company_id)
        elif region_name != ' ':
            # filter images by region
            query = Turbines.query.filter_by(region_id = region_id, company_id = company_id)
        elif park_name != ' ':
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
    return make_response(jsonify({'turbines': [{'turbine': turbine.json(), 'pinned': PinnedTurbines.query.filter_by(turbine_id=turbine.id).first() is not None, 'region': Regions.query.filter_by(id=turbine.region_id).first().region, 'park': Parks.query.filter_by(id=turbine.park_id).first().park} for turbine in query]}), 200)

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

'''----- search using turbine name----- '''
@api.route('/search_turbine/<search_term>', methods=['GET'])
def search_turbine(search_term):
    try:
        if current_user.company_id == None:
            return make_response(jsonify({'message': 'not assigned to a company'}), 500)
        company_id = Companies.query.filter_by(id=current_user.company_id).first().id
        turbines = Turbines.query.filter(Turbines.turbine.ilike('%' + search_term + '%'), Turbines.company_id == company_id).all()
        api.logger.info('Turbines: %s', turbines)
        return make_response(jsonify({'turbines': [{'turbine': turbine.json(), 'pinned': PinnedTurbines.query.filter_by(turbine_id=turbine.id).first() is not None, 'region': Regions.query.filter_by(id=turbine.region_id).first().region, 'park': Parks.query.filter_by(id=turbine.park_id).first().park} for turbine in turbines]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error searching for turbines', 'error': str(e)}), 500)


'''----- get pinned turbines -----'''
@api.route('/get_pinned', methods=['GET'])
def get_pinned():
    try:
        if current_user.company_id == None:
            return make_response(jsonify({'message': 'not assigned to a company'}), 500)
        company_id = Companies.query.filter_by(id=current_user.company_id).first().id
        pinned_turbines = PinnedTurbines.query.filter_by(user_id=current_user.id, company_id = company_id).all()
        api.logger.info('Pinned turbines: %s', pinned_turbines)
        if len(pinned_turbines) > 0:
            return make_response(jsonify({'pinned_turbines': [{'turbine_id': pinned_turbine.turbine_id, 'name': get_turbine_name(pinned_turbine.turbine_id)} for pinned_turbine in pinned_turbines], 'empty':False}), 200)
        return make_response(jsonify({'message': 'No pinned turbines', 'empty': True}), 200)
    except Exception as e:
        api.logger.error(e)
        return make_response(jsonify({'message': 'error getting pinned turbines', 'error': str(e)}), 500)
    
get_turbine_name = lambda id: Turbines.query.filter_by(id=id).first().turbine

'''----- pin turbine -----'''
@api.route('/pin_turbine/<turbine_id>', methods=['GET'])
def pin_turbine(turbine_id):
    try:
        present_turbine = PinnedTurbines.query.filter_by(turbine_id=turbine_id).first()
        if present_turbine:
            return make_response(jsonify({'message': 'Turbine already pinned', 'already_pinned': True}), 200)
        turbine = PinnedTurbines(turbine_id=turbine_id, user_id=current_user.id, company_id = current_user.company_id)
        db.session.add(turbine)
        db.session.commit()
        return make_response(jsonify({'message': 'Turbine pinned successfully', 'already_pinned': False}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error pinning turbine', 'error': str(e)}), 500)
    
'''----- unpin turbine -----'''
@api.route('/unpin_turbine/<turbine_id>', methods=['GET'])
def unpin_turbine(turbine_id):
    try:
        turbine = PinnedTurbines.query.filter_by(turbine_id=turbine_id, user_id=current_user.id, company_id = current_user.company_id).first()
        db.session.delete(turbine)
        db.session.commit()
        return make_response(jsonify({'message': 'Turbine unpinned successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error unpinning turbine', 'error': str(e)}), 500)
    

'''----- Get all weather data for turbine -----'''
@api.route('/weather_data/<turbine_id>', methods=['GET'])
def weather_data(turbine_id):
    try:
        turbine = Turbines.query.filter_by(id=turbine_id).first()
        weather_data = WeatherData.query.filter_by(park_id=turbine.park_id).all()
        return make_response(jsonify({'weather_data': [data.json() for data in weather_data]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting weather data', 'error': str(e)}), 500)


'''
================== !LOCATIONS ==================
'''

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



'''
================== !USER ==================
'''

'''----- Validate user -----'''
def valid_login(email, password):
    # Check if the email exists in the database
    user = db.session.query(Users).filter_by(email=email).first()
    if user is None:
        return False
    else:
        return check_password_hash(user.password, password)
    
'''----- Change password -----'''
@api.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    # Check if the current password is correct
    if check_password_hash(current_user.password, current_password):
        # Update the user's password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('account_page'))
    else:
        flash('Current password is incorrect.')
        return redirect(url_for('change_password'))

'''----- Index/login route -----'''
@api.route('/', methods=['GET', 'POST'])
# @login_required OM MAN VILL GÖRA SÅ MAN INTE KOMMER IN UTAN INLOGGNING
def home():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()
        print("============ TRYING TO LOGIN ============")
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("search_page"))
        else:
            print(" ================ Wrong email or password  ================ ")
            error = 'Invalid email or password'
    return render_template("login.html", error=error)

'''----- Logout route -----'''
@api.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

'''----- Register page -----'''
@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        user = Users(email=email, password=hashed_password, privilege="0", company_id="1")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")

'''----- Change theme -----'''
@api.route('/change_theme', methods=['POST'])
def change_theme():
    theme = request.form.get('theme')
    user = Users.query.get(current_user.id)
    old_theme = user.theme
    user.theme = theme
    db.session.commit()
    if old_theme != theme:
        return jsonify({'status': 'success', 'message': 'Theme changed'})
    else:
        return jsonify({'status': 'success', 'message': 'Theme not changed'})
    
'''----- Change language -----'''
@api.route('/change_language', methods=['POST'])
@login_required
def change_language():
    lang = request.form.get('lang')
    user = Users.query.get(current_user.id)
    old_lang = user.language
    user.language = lang
    db.session.commit()
    if old_lang != lang:
        return jsonify({'status': 'success', 'message': 'Language changed'})
    else:
        return jsonify({'status': 'success', 'message': 'Language not changed'})

'''
=================== PAGES ===================
'''

'''----- Get Search page -----'''
@api.route('/search_page', methods=['GET'])
@login_required
def search_page():
    user = Users.query.get(current_user.id)
    return render_template('search.html', user=user)


'''----- Get Account page -----'''
@api.route('/account', methods=['GET'])
@login_required
def account_page():
    user = Users.query.get(current_user.id)
    return render_template('account.html', user=user)


'''----- Get turbine page -----'''
@api.route('/turbine/<turbineId>', methods=['GET'])
@login_required
def turbine_page(turbineId):
    turbine = Turbines.query.get(turbineId)
    api.logger.info('Turbine ID: %s', turbine.id)
    region = Regions.query.get(turbine.region_id).region
    park = Parks.query.get(turbine.park_id).park
    latest_image = ImageUrl.query.filter_by(turbine_id=turbineId).order_by(ImageUrl.datetime.desc()).first()
    isPinned = PinnedTurbines.query.filter_by(turbine_id=turbineId, user_id=current_user.id, company_id = current_user.company_id).first() is not None
    weather_data = WeatherData.query.filter_by(park_id=turbine.park_id).order_by(WeatherData.validtime.desc()).first()
    return render_template('turbine.html', turbineId=turbine.id, turbineRegion=region, turbinePark=park, turbineName=turbine.turbine, isPinned = isPinned, turbineImage=latest_image, user=current_user, weather_data=weather_data)

'''----- Get settings page -----'''
@api.route('/settings', methods=['GET'])
@login_required
def settings_page():
    user = Users.query.get(current_user.id)
    return render_template('settings.html', user=user)

'''----- Get help and support page -----'''
@api.route('/help-support', methods=['GET'])
@login_required
def help_support():
    user = Users.query.get(current_user.id)
    return render_template('help-support.html', user=user)

@api.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return "An internal server error occurred.", 500

try:
    # Your existing code to start the Flask application
    logging.info('Starting application...')
    api.run(host='0.0.0.0', port=4000)
except Exception as e:
    logging.exception('Failed to start application')