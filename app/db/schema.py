from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import environ
from flask import Flask
db = SQLAlchemy()
# Table for companies
class Companies(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=True, nullable=False)

    regions = db.relationship('Regions', lazy=True)
    parks = db.relationship('Parks', lazy=True)
    turbines = db.relationship('Turbines', lazy=True)
    users = db.relationship('Users', lazy=True)
    pinned_turbines = db.relationship('PinnedTurbines', lazy=True)

    def __init__(self, company):
        self.company = company

    def json(self):
        return {'id': self.id, 'company': self.company}

# Table for regions
class Regions(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)

    parks = db.relationship('Parks', lazy=True)
    turbines = db.relationship('Turbines', lazy=True)

    def __init__(self, region, company_id):
        self.region = region
        self.company_id = company_id
        

    def json(self):
        return {'id': self.id, 'region': self.region, 'company_id': self.company_id}

# Table for parks
class Parks(db.Model):
    __tablename__ = 'parks'

    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.String(255), nullable=False)
    coordinates = db.Column(db.String(30), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(Regions.id), nullable=False)

    turbines = db.relationship('Turbines', lazy=True)
    weather_data = db.relationship('WeatherData', lazy=True)

    def __init__(self, park, company_id, region_id, coordinates):
        self.park = park
        self.company_id = company_id
        self.region_id = region_id
        self.coordinates = coordinates

    def json(self):
        return {'id': self.id, 'park': self.park, 'region_id': self.region_id,
                'company_id': self.company_id, 'coordinates': self.coordinates}


# Table for turbines
class Turbines(db.Model):
    __tablename__ = 'turbines'

    id = db.Column(db.Integer, primary_key=True)
    turbine = db.Column(db.String(255), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(Regions.id), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey(Parks.id), nullable=False)
    
    image_url = db.relationship('ImageUrl', lazy=True)

    def __init__(self, turbine, company_id, region_id, park_id):
        self.turbine = turbine
        self.company_id = company_id
        self.region_id = region_id
        self.park_id = park_id

    def json(self):
        return {'id': self.id, 'turbine': self.turbine, 'park_id': self.park_id, 'region_id': self.region_id, 'company_id': self.company_id}

# Table for users
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    privilege = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=True)
    language = db.Column(db.String(20), nullable=False, default='eng')

    PinnedTurbines = db.relationship('PinnedTurbines', lazy=True)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    validtime = db.Column(db.String(30), nullable=False)
    date_hour = db.Column(db.String(30), nullable=False)
    request_coordinates = db.Column(db.String(30))
    fetched_coordinates = db.Column(db.String(30))
    msl = db.Column(db.Numeric(6, 1))
    t = db.Column(db.Numeric(6, 1))
    vis = db.Column(db.Numeric(6, 1))
    wd = db.Column(db.Integer)
    ws = db.Column(db.Numeric(6, 1))
    r = db.Column(db.Integer)
    tstm = db.Column(db.Integer)
    tcc_mean = db.Column(db.Integer)
    lcc_mean = db.Column(db.Integer)
    mcc_mean = db.Column(db.Integer)
    hcc_mean = db.Column(db.Integer)
    gust = db.Column(db.Numeric(6, 1))
    pmin = db.Column(db.Numeric(6, 1))
    pmax = db.Column(db.Numeric(6, 1))
    spp = db.Column(db.Integer)
    pcat = db.Column(db.Integer)
    pmean = db.Column(db.Numeric(6, 1))
    pmedian = db.Column(db.Numeric(6, 1))
    Wsymb2 = db.Column(db.Integer)
    park_id = db.Column(db.Integer, db.ForeignKey(Parks.id), nullable=False)
    image_url = db.relationship('ImageUrl', lazy=True)

    def __init__(self, validtime, date_hour, request_coordinates, fetched_coordinates, msl, t, vis, wd, ws, r, tstm,
                 tcc_mean, lcc_mean, mcc_mean, hcc_mean, gust, pmin, pmax, spp, pcat, pmean, pmedian, Wsymb2, park_id):
        self.validtime = validtime
        self.date_hour = date_hour
        self.request_coordinates = request_coordinates
        self.fetched_coordinates = fetched_coordinates
        self.msl = msl
        self.t = t
        self.vis = vis
        self.wd = wd
        self.ws = ws
        self.r = r
        self.tstm = tstm
        self.tcc_mean = tcc_mean
        self.lcc_mean = lcc_mean
        self.mcc_mean = mcc_mean
        self.hcc_mean = hcc_mean
        self.gust = gust
        self.pmin = pmin
        self.pmax = pmax
        self.spp = spp
        self.pcat = pcat
        self.pmean = pmean
        self.pmedian = pmedian
        self.Wsymb2 = Wsymb2
        self.park_id = park_id

    def json(self):
        return {'validtime': self.validtime, 'date_hour': self.date_hour, 'request_coordinates': self.request_coordinates,
                'fetched_coordinates': self.fetched_coordinates, 'msl': self.msl, 't': self.t, 'vis': self.vis, 'wd': self.wd,
                'ws': self.ws, 'r': self.r, 'tstm': self.tstm, 'tcc_mean': self.tcc_mean, 'lcc_mean': self.lcc_mean,
                'mcc_mean': self.mcc_mean, 'hcc_mean': self.hcc_mean, 'gust': self.gust, 'pmin': self.pmin, 'pmax': self.pmax,
                'spp': self.spp, 'pcat': self.pcat, 'pmean': self.pmean, 'pmedian': self.pmedian, 'Wsymb2': self.Wsymb2,
                'park_id': self.park_id}

# Table for image urls
class ImageUrl(db.Model):
    __tablename__ = 'image_url'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(255), nullable=False)
    date_hour = db.Column(db.String(255), nullable=False)
    camera1_url = db.Column(db.String(255))
    camera2_url = db.Column(db.String(255))
    turbine_id = db.Column(db.Integer, db.ForeignKey(Turbines.id), nullable=False)
    weather_id = db.Column(db.Integer, db.ForeignKey(WeatherData.id), nullable=False)

    def __init__(self, datetime, date_hour, camera1_url, camera2_url, turbine_id, weather_id):
        self.datetime = datetime
        self.date_hour = date_hour
        self.camera1_url = camera1_url
        self.camera2_url = camera2_url
        self.turbine_id = turbine_id
        self.weather_id = weather_id

    def json(self):
        return {'camera1_url': self.camera1_url, 'camera2_url': self.camera2_url, 'datetime': self.datetime,
                'date_hour': self.date_hour, 'turbine_id': self.turbine_id}


# Table for pinned turbines
class PinnedTurbines(db.Model):
    __tablename__ = 'pinned_turbines'

    id = db.Column(db.Integer, primary_key=True)
    turbine_id = db.Column(db.Integer, db.ForeignKey(Turbines.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)

    def __init__(self, turbine_id, user_id, company_id):
        self.turbine_id = turbine_id
        self.user_id = user_id
        self.company_id = company_id

    def json(self):
        return {'id': self.id,'turbine_id': self.turbine_id, 'user_id': self.user_id}
    
