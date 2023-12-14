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
    url = db.Column(db.String(120), nullable=False)
    turbine = db.Column(db.String(50), nullable=False, foreign_key=True)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, url, turbine, date):
        self.url = url
        self.turbine = turbine
        self.date = date

    def json(self):
        return {'id': self.id, 'url': self.url, 'turbine': self.turbine, 'date': self.date}

