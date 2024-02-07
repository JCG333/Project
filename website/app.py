from os import urandom
from flask import *
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash
from db.schema import db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userdb'  # Test

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def load_users():
    if current_user.is_authenticated:
        return current_user.username
    else:
        return "Guest"


@app.route('/')
# @login_required OM MAN VILL GÖRA SÅ MAN INTE KOMMER IN UTAN INLOGGNING
def home():
    data = {
        'title': 'Service for snow and ice detection',
        'header': 'Service for snow and ice detection',
        'welcome_message': 'Welcome to the service for snow and ice detection!',
        'user': load_users(),
        'content': 'Contents',
        'footer_text': 'Service for snow and ice detection. All rights reserved.'
    }
    return render_template('index.html', **data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        user = Users(username=username, password=hashed_password, privilege="0")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/turbine")
def turbine():
    return render_template("turbinePage.html")


if __name__ == '__main__':
    app.run(debug=True)
