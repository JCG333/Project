'''
Filename: schema.py

This is the schema for the database and contains the tables that will be created in the database. 
The tables are:
    - companies
    - regions
    - parks
    - turbines
    - images
'''

from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Table for specific images
class images(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(120), nullable=False)
    region = db.Column(db.String(120), nullable=False)
    park = db.Column(db.String(120), nullable=False)
    turbine = db.Column(db.String(120), nullable=False)
    

    def __init__(self, url, turbine, date, company, region, park):
        self.url = url
        self.date = date
        self.company = company
        self.region = region
        self.park = park
        self.turbine = turbine
        

    def json(self):
        return {
                'id': self.id, 
                'url': self.url,
                'turbine': self.turbine,
                'date': self.date,
                'company': self.company,
                'region': self.region,
                'park': self.park
                }


