from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(Regions.id), nullable=False)

    turbines = db.relationship('Turbines', lazy=True)

    def __init__(self, park, company_id, region_id):
        self.park = park
        self.company_id = company_id
        self.region_id = region_id

    def json(self):
        return {'id': self.id, 'park': self.park, 'region_id': self.region_id, 'company_id': self.company_id}

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

# Table for image urls
class ImageUrl(db.Model):
    __tablename__ = 'image_url'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), unique=True, nullable=False)
    weather_data = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.String(255), nullable=False)
    turbine_id = db.Column(db.Integer, db.ForeignKey(Turbines.id), nullable=False)

    def __init__(self, image_url, weather_data, date_time, turbine_id):
        self.image_url = image_url
        self.weather_data = weather_data
        self.date_time = date_time
        self.turbine_id = turbine_id

    def json(self):
        return {'image_url': self.image_url, 'turbine_id': self.turbine_id}

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
    
# Table for users
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    privilege = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=True)
    language = db.Column(db.String(20), nullable=False, default='eng')

    PinnedTurbines = db.relationship('PinnedTurbines', lazy=True)

# If, and probably when we need weather data table:
#
# class WeatherData(db.Model):
#     __tablename__ = 'image_url'
#     __table_args__ = {'schema': 'snowice'}

#     id = db.Column(db.Integer, primary_key=True)



# with app.app_context():
#     # Create Table
#     db.create_all()


# with app.app_context():
#     company = Companies(company='Vattenfall')
#     db.session.add(company)
#     db.session.commit()
#     region = Regions(region='Sweden', company_id=company.id)
#     db.session.add(region)
#     db.session.commit()
#     park = Parks(park='Juktan', company_id=company.id, region_id=region.id)
#     db.session.add(park)
#     db.session.commit()
#     turbine = Turbines(turbine='AAA001', park_id=park.id, region_id=region.id, company_id=company.id)
#     db.session.add(turbine)
#     db.session.commit()
#     image = ImageUrl(image_url='company/region/park/turbines/AAA001-20240116-h09m27.png', weather_data='cloudy with a chance of meatballs', date_time='20240118-h09m27', turbine_id=turbine.id)
#     db.session.add(image)
#     db.session.commit()

# Console commands to push database from python console:
#   console/~$ python
#   >>> from pythonfile import app, db
#   >>> app.app_context().push()
#   >>> db.create_all()