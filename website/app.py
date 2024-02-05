from os import urandom
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from db.schema import Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'
app.config["SECRET_KEY"] = urandom(20)
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)




@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def home():
    data = {
        'title': 'Service for snow and ice detection',
        'header': 'Service for snow and ice detection',
        'welcome_message': 'Welcome to the service for snow and ice detection!',
        'content': 'Contents',
        'footer_text': 'Service for snow and ice detection. All rights reserved.'
    }
    return render_template('index.html', **data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"),
                     privilege="0")
        db.session.add(user)
        db.session.commit()
        return redirect("login")
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
