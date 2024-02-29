import requests
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'

from db.schema import db, Parks, WeatherData


# Reads the values from the json format and returns a dict with the values in order of appearance
def get_weather_data():
    with app.app_context():
        # Gets the coordinates for all the parks in schema.Parks table
        park_info = db.session.query(Parks.id, Parks.coordinates).all()
        for info in park_info:
            park_id = info[0]
            request_coordinates = info[1]
            coordinates = request_coordinates.split(',')
            lat, lon = coordinates[0], coordinates[1]

            request_url = ('https://opendata-download-metfcst.smhi.se/api/category'
                           '/pmp3g/version/2/geotype/point/lon/'+lon+'/lat/'+lat+'/data.json')

            response = requests.get(request_url)
            # print('Response status: --> ' + str(response.status_code) + ' <-- code 200 means OK!')
            response_json = json.loads(response.text)

            fetched_coordinates = (str(response_json['geometry']['coordinates'][0][1]) + ','
                                   + str(response_json['geometry']['coordinates'][0][0]))

            # Because of the way SMHI approves forecasts, two hours must be fetched and compared after update of approved time
            # forecast_data_1 contains the forecast for this hour (validtime format is yyyy-mm-ddThh:mm:ssZ)
            forecast_data_1 = {
                'validtime': str(response_json['timeSeries'][0]['validTime']),
                'request_coordinates': request_coordinates,
                'fetched_coordinates': fetched_coordinates,
            }

            # forecast_data_2 contains data for the next hour
            forecast_data_2 = {
                'validtime': str(response_json['timeSeries'][1]['validTime']),
                'request_coordinates': request_coordinates,
                'fetched_coordinates': fetched_coordinates,
            }

            # These loops add the name of the type of weather data and its corresponding value into a dict
            i = 0
            while i < len(response_json['timeSeries'][0]['parameters']):
                forecast_data_1[response_json['timeSeries'][0]['parameters'][i]['name']] = (
                    response_json)['timeSeries'][0]['parameters'][i]['values'][0]
                i += 1

            i = 0
            while i < len(response_json['timeSeries'][0]['parameters']):
                forecast_data_2[response_json['timeSeries'][1]['parameters'][i]['name']] = (
                    response_json)['timeSeries'][1]['parameters'][i]['values'][0]
                i += 1

            add_weather_data(forecast_data_1, forecast_data_2, response_json, park_id)


def update_forecast_one(forecast_data_1, park_id):
    # Updates most recent hour from SMHI's weather data if it exists in database
    with app.app_context():
        db.session.query(WeatherData).filter(
            WeatherData.park_id == park_id, WeatherData.validtime == forecast_data_1['validtime']).update(forecast_data_1)
        db.session.commit()


def add_forecast_one(forecast_data_1, park_id):
    # print('Forecast 1: Adding weather data for ' + str(forecast_data_1['validtime']) + ' at park_id '+str(park_id))
    with app.app_context():

        weather_info = WeatherData(
            validtime=forecast_data_1['validtime'],
            # date_hour is part of the string validtime to be able to query weather data by hour
            # and has format 'yyyy-mm-ddThh'
            date_hour=forecast_data_1['validtime'][:13],
            request_coordinates=forecast_data_1['request_coordinates'],
            fetched_coordinates=forecast_data_1['fetched_coordinates'],
            spp=forecast_data_1['spp'],
            pcat=forecast_data_1['pcat'],
            pmin=forecast_data_1['pmin'],
            pmean=forecast_data_1['pmean'],
            pmax=forecast_data_1['pmax'],
            pmedian=forecast_data_1['pmedian'],
            tcc_mean=forecast_data_1['tcc_mean'],
            lcc_mean=forecast_data_1['lcc_mean'],
            mcc_mean=forecast_data_1['mcc_mean'],
            hcc_mean=forecast_data_1['hcc_mean'],
            t=forecast_data_1['t'],
            msl=forecast_data_1['msl'],
            vis=forecast_data_1['vis'],
            wd=forecast_data_1['wd'],
            ws=forecast_data_1['ws'],
            r=forecast_data_1['r'],
            tstm=forecast_data_1['tstm'],
            gust=forecast_data_1['gust'],
            Wsymb2=forecast_data_1['Wsymb2'],
            park_id=park_id)

        db.session.add(weather_info)
        db.session.commit()


def add_forecast_two(forecast_data_2, park_id):
    # print('Forecast 2: Adding weather data for ' + str(forecast_data_2['validtime']) + ' at park id '+str(park_id))
    with app.app_context():

        weather_info = WeatherData(
            validtime=forecast_data_2['validtime'],
            # date_hour is part of the string validtime to be able to query weather data by hour
            # and has format 'yyyy-mm-ddThh'
            date_hour=forecast_data_2['validtime'][:13],
            request_coordinates=forecast_data_2['request_coordinates'],
            fetched_coordinates=forecast_data_2['fetched_coordinates'],
            spp=forecast_data_2['spp'],
            pcat=forecast_data_2['pcat'],
            pmin=forecast_data_2['pmin'],
            pmean=forecast_data_2['pmean'],
            pmax=forecast_data_2['pmax'],
            pmedian=forecast_data_2['pmedian'],
            tcc_mean=forecast_data_2['tcc_mean'],
            lcc_mean=forecast_data_2['lcc_mean'],
            mcc_mean=forecast_data_2['mcc_mean'],
            hcc_mean=forecast_data_2['hcc_mean'],
            t=forecast_data_2['t'],
            msl=forecast_data_2['msl'],
            vis=forecast_data_2['vis'],
            wd=forecast_data_2['wd'],
            ws=forecast_data_2['ws'],
            r=forecast_data_2['r'],
            tstm=forecast_data_2['tstm'],
            gust=forecast_data_2['gust'],
            Wsymb2=forecast_data_2['Wsymb2'],
            park_id=park_id)

        db.session.add(weather_info)
        db.session.commit()


def add_weather_data(forecast_data_1, forecast_data_2, response_json, park_id):
    print('adding weather data')
    with app.app_context():

        query_result_1 = db.session.query(WeatherData).filter_by(
            validtime=response_json['timeSeries'][0]['validTime'], park_id=park_id).first() is not None
        query_result_2 = db.session.query(WeatherData).filter_by(
            validtime=response_json['timeSeries'][1]['validTime'], park_id=park_id).first() is not None

        # If-statements to check if there are already entries for the park id and validtime.
        # If an entry already exists for the earliest time given by SMHI, it updates.
        # Otherwise it adds weather data for the earliest hour and the following hour to the database.
        if query_result_1:
            update_forecast_one(forecast_data_1, park_id)
            if query_result_2:
                pass
            else:
                add_forecast_two(forecast_data_2, park_id)
        else:
            add_forecast_one(forecast_data_1, park_id)
            if query_result_2:
                pass
            else:
                add_forecast_two(forecast_data_2, park_id)
