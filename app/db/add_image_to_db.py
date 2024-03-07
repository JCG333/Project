from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import re
from os import environ
import logging

logging.basicConfig(level=logging.INFO)

from api import api

from db.schema import db, Turbines, ImageUrl, WeatherData, Parks

def extract_datetime(img_url):
    # Defines a regular expression pattern to match the desired datetime format
    pattern = r'(?:[^/]+)?\d{2}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\b'

    # Search for the pattern in the URL
    match = re.search(pattern, img_url)
    if match:
        logging.info('HEJ!!!!!')
        # Extract the matched datetime string
        # Ensure to extract the last 17 characters
        datetime_str = match.group().replace('-', '').replace('_', '')
        # Format the datetime string as ('YYYY-MM-DDTHH:MM:SSZ')
        format_datetime = ('20'+datetime_str[0:2]+'-'+datetime_str[2:4]+'-'+datetime_str[4:6]+'T'+datetime_str[6:8]
                           +':'+datetime_str[8:10]+':'+datetime_str[10:12]+'Z')
        # Format the date_hour string as ('YYYY-MM-DDTHH')
        date_hour = format_datetime[:13]
        # print(format_datetime, date_hour)
        return format_datetime, date_hour
    else:
        logging.info('no match found!!!!')
        return None  # Return None if no match is founnd

def parse_url(info):
    # Extract information about park, turbine, etc. from the URL
    info = info.split('/')
    if (info is None) or (len(info) == 0):
        logging.info('no url parese') 
    return info[2], info[3], info[4], info[-1]


def add_data(image_url):

    park, turbine, camera, date = parse_url(image_url)
    logging.info('park: %s, turbine: %s, camera: %s, date: %s', park, turbine, camera, date)
    date_time, date_hour = extract_datetime(date)
    # print('add_data function:', data, raw_data, park, turbine, camera, date_time, date_hour)
    with api.app_context():
        # Check if turbine, park and URL exists
        turbine_exists = db.session.query(Turbines.id).filter_by(turbine=turbine).first() is not None
        logging.info('turbine exists: %s', turbine_exists)
        url_exists = db.session.query(ImageUrl.id).filter(
            (ImageUrl.camera1_url == image_url) | (ImageUrl.camera2_url == image_url)).first() is not None
        park_exists = db.session.query(Parks.id).filter(Parks.park == park).first() is not None
        if park_exists:
            logging.info('PARK EXISTS!!!!!!!!!!!')
            # Check if weather entry exists for hour and park requested
            park_exists = db.session.query(Parks.id).filter(Parks.park == park).first()
            weather_exists = db.session.query(WeatherData.id).filter(WeatherData.date_hour == date_hour,
                                                                 WeatherData.park_id == park_exists[0]).first() is not None
            logging.info('weather exists: %s', weather_exists)
            if turbine_exists and weather_exists:
                logging.info('YAY! TURBINE EXISTS!!!!!!!!')
                # Fetch turbine and weather id belonging to image
                turbine_exists = db.session.query(Turbines.id).filter_by(turbine=turbine).first()
                weather_exists = db.session.query(WeatherData.id).filter(WeatherData.date_hour == date_hour,
                                                                     WeatherData.park_id == park_exists[0]).first()
                print(weather_exists[0])
                if url_exists:
                    print('Image already exists in database')
                else:
                    if camera == 'Camera1':
                        image = ImageUrl(camera1_url=image_url[36:], camera2_url=None,
                                         datetime=date_time, date_hour=date_hour, turbine_id=turbine_exists[0],
                                         weather_id=weather_exists[0])
                        logging.info('Camera1 image here %s', image)
                        db.session.add(image)
                        db.session.commit()
                    if camera == 'Camera2':
                        image = ImageUrl(camera2_url=image_url[36:], camera1_url=None,
                                         datetime=date_time, date_hour=date_hour, turbine_id=turbine_exists[0],
                                         weather_id=weather_exists[0])
                        db.session.add(image)
                        db.session.commit()
            else:
                logging.info('Turbine or weather data does not exist')
