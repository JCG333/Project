from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/Userdb'

db = SQLAlchemy(app)


class Companies(db.Model):
    __tablename__ = 'companies'
    __table_args__ = {'schema': 'snowice'}

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=True, nullable=False)
    regions = db.relationship('Regions', lazy=True)
    parks = db.relationship('Parks', lazy=True)
    turbines = db.relationship('Turbines', lazy=True)

    def json(self):
        return {'id': self.id, 'company': self.company}


class Regions(db.Model):
    __tablename__ = 'regions'
    __table_args__ = {'schema': 'snowice'}

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    parks = db.relationship('Parks', lazy=True)
    turbines = db.relationship('Turbines', lazy=True)

    def json(self):
        return {'id': self.id, 'region': self.region, 'company_id': self.company_id}


class Parks(db.Model):
    __tablename__ = 'parks'
    __table_args__ = {'schema': 'snowice'}

    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(Regions.id), nullable=False)
    turbines = db.relationship('Turbines', lazy=True)

    def json(self):
        return {'id': self.id, 'park': self.park, 'region_id': self.region_id, 'company_id': self.company_id}


class Turbines(db.Model):
    __tablename__ = 'turbines'
    __table_args__ = {'schema': 'snowice'}

    id = db.Column(db.Integer, primary_key=True)
    turbine = db.Column(db.String(255), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(Companies.id), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(Regions.id), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey(Parks.id), nullable=False)
    image_url = db.relationship('ImageUrl', lazy=True)

    def json(self):
        return {'id': self.id, 'turbine': self.turbine, 'park_id': self.park_id, 'region_id': self.region_id, 'company_id': self.company_id}


class ImageUrl(db.Model):
    __tablename__ = 'image_url'
    __table_args__ = {'schema': 'snowice'}

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), unique=True, nullable=False)
    weather_data = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.String(255), nullable=False)
    turbine_id = db.Column(db.Integer, db.ForeignKey(Turbines.id), nullable=False)

    def json(self):
        return {'image_url': self.image_url, 'turbine_id': self.turbine_id}


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
