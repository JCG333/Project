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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'  # test
# Initialize the database instance
db = SQLAlchemy(app)


class WindTurbine(db.Model):
    __tablename__ = 'turbine_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String(120), nullable=False)
    region = db.Column(db.String(120), nullable=False)
    turbine = db.Column(db.String(120), nullable=False)

    def __init__(self, company, region, turbine):
        self.company = company
        self.region = region
        self.turbine = turbine

    def json(self):
        return {'id': self.id, 'company': self.company, 'region': self.region, 'turbine': self.turbine}


def addData(company, region, turbine):
    with app.app_context():
        new_data = WindTurbine(company=company, region=region, turbine=turbine)
        db.session.add(new_data)
        db.session.commit()


with app.app_context():
    # Create Table
    db.create_all()

    # test data
    # test_image_1 = images(company='hej', region='hej', turbine='tja')
    # test_image_2 = images(company='tja', region='hje', turbine='yes')

    # db.session.add(test_image_1)
    # db.session.add(test_image_2)

    # db.session.commit()

#  if __name__ == '__main__':  # testar
    #  app.run(debug=True)
    #  addData("company", "region", "turbine")  # testar lägga in i databasen
