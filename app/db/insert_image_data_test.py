from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/Userdb'

db = SQLAlchemy(app)

def parse_info(info):
    # Parse the URL and image name for the info needed to add to database (this might be overkill)
    splitsymbols = ['/', '-', '.']

    for symbol in splitsymbols:
        info = " ".join(info.split(symbol))

    info = info.split()
    return info[0], info[1], info[2], info[4], info[5]+'-'+info[6]

def add_data(img_url, weather_data):
    # Maybe some sort of try clause?
    # try:
    #     something
    # except:
    #     It didn't work

    company, region, park, turbine, date_time = parse_info(img_url)

    with app.app_context():
        # Makes a query if URL with this name exists. url_exists = True if it exists
        url_exists = db.session.query(schema.ImageUrl.id).filter_by(image_url=img_url).first() is not None
        # Makes a query if URL with this name exists. turbine_exists = True if it exists
        turbine_exists = db.session.query(schema.Turbines.id).filter_by(turbine=turbine).first() is not None

        if turbine_exists:
            # Makes query to get the ID with this turbines name.
            # Returns a tuple for some reason so ID must be given from index in tuple when making entry to database
            # as seen in the else clause.
            turbine_id_tuple = db.session.query(schema.Turbines.id).filter(schema.Turbines.turbine == turbine).first()
            if url_exists:
                return print('Image already in database.')
            else:
                new_image = schema.ImageUrl(image_url=img_url, weather_data=weather_data, date_time=date_time, turbine_id=turbine_id_tuple[0])
                db.session.add(new_image)
                db.session.commit()
        else:
            print(turbine + ' does not exist in database. Make sure name is correct.')

# URLs will be changed and also maybe weather data
add_data('vattenfall/sweden/juktan/images/AAA001-20240118-h12m15.png', 'very much snow and ice')
