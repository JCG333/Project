from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.schema import Turbines, ImageUrl, WeatherData, Parks
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'

db = SQLAlchemy(app)


def extract_datetime(img_url):
    # Defines a regular expression pattern to match the desired datetime format
    pattern = r'(?:[^/]+)?\d{2}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\b'

    # Search for the pattern in the URL
    match = re.search(pattern, img_url)

    if match:
        # Extract the matched datetime string
        datetime_str = match.group()[len(match.group()) - 17:]  # Ensure to extract the last 17 characters
        datetime_str = datetime_str.replace('-', '').replace('_', '')
        # Format the datetime string as ('YYYY-MM-DDTHH:MM:SSZ')
        format_datetime = ('20'+datetime_str[0:2]+'-'+datetime_str[2:4]+'-'+datetime_str[4:6]+'T'+datetime_str[6:8]
                           +':'+datetime_str[8:10]+':'+datetime_str[10:12]+'Z')
        # Format the date_hour string as ('YYYY-MM-DDTHH')
        date_hour = format_datetime[:13]
        # print(format_datetime, date_hour)
        return format_datetime, date_hour
    else:
        return None  # Return None if no match is found


def parse_url(info):
    # Extract information about park, turbine, etc. from the URL
    info = info.split('/')
    return info[1], info[2], info[3], info[4], info[5]


def add_data(image_url):

    data, raw_data, park, turbine, camera = parse_url(image_url)
    date_time, date_hour = extract_datetime(image_url)

    # print('add_data function:', data, raw_data, park, turbine, camera, date_time, date_hour)
    with app.app_context():
        # Check if turbine, park and URL exists
        turbine_exists = db.session.query(Turbines.id).filter_by(turbine=turbine).first() is not None
        url_exists = db.session.query(ImageUrl.id).filter(
            (ImageUrl.camera1_url == image_url) | (ImageUrl.camera2_url == image_url)).first() is not None
        park_exists = db.session.query(Parks.id).filter(Parks.park == park).first() is not None
        if park_exists:
            # Check if weather entry exists for hour and park requested
            park_exists = db.session.query(Parks.id).filter(Parks.park == park).first()
            weather_exists = db.session.query(WeatherData.id).filter(WeatherData.date_hour == date_hour,
                                                                 WeatherData.park_id == park_exists[0]).first() is not None
            if turbine_exists and weather_exists:
                # Fetch turbine and weather id belonging to image
                turbine_exists = db.session.query(Turbines.id).filter_by(turbine=turbine).first()
                weather_exists = db.session.query(WeatherData.id).filter(WeatherData.date_hour == date_hour,
                                                                     WeatherData.park_id == park_exists[0]).first()
                print(weather_exists[0])
                if url_exists:
                    print('Image already exists in database')
                else:
                    if camera == 'Camera1':
                        image = ImageUrl(camera1_url=image_url, camera2_url=None,
                                         datetime=date_time, date_hour=date_hour, turbine_id=turbine_exists[0],
                                         weather_id=weather_exists[0])
                        db.session.add(image)
                        db.session.commit()
                    if camera == 'Camera2':
                        image = ImageUrl(camera2_url=image_url, camera1_url=None,
                                         datetime=date_time, date_hour=date_hour, turbine_id=turbine_exists[0],
                                         weather_id=weather_exists[0])
                        db.session.add(image)
                        db.session.commit()
            else:
                print('Something went wrong, make sure turbine or weather you\'re trying to query exists in database.')