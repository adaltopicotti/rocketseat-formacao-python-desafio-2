import binascii
from datetime import datetime
import os
import sys
import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate
from database import db
from models.user import User
from models.meal import Meal

load_dotenv()

CONFIG_SECRET_KEY = os.getenv("CONFIG_SECRET_KEY")
CONFIG_DATABASE_URI = os.getenv("CONFIG_DATABASE_URI")

READY_TO_RUN = True
if not CONFIG_SECRET_KEY:
    print("* Secret key not found")
    READY_TO_RUN = False
if not CONFIG_DATABASE_URI:
    print("* Invalid database")
    READY_TO_RUN = False

app = Flask(__name__)


if READY_TO_RUN:
    app.config['SECRET_KEY'] = CONFIG_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG_DATABASE_URI

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    # view login
    login_manager.login_view = 'login'
else:
    sys.exit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username", None)
    password = data.get("password", None)

    if username and password:
        user = User.query.filter_by(username=username).first()

        byte_value = binascii.unhexlify(user.password[2:])

        if user and bcrypt.checkpw(str.encode(password), byte_value):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username", None)
    password = data.get("password", None)

    if username and password:

        hashed_password = bcrypt.hashpw(
            str.encode(password),
            bcrypt.gensalt()
        )

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400


@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    name = data.get("name", None)
    description = data.get("description", None)
    in_diet = data.get("in_diet", None)

    if name and description and in_diet is not None:

        current_time = datetime.now()
        print(current_user)
        meal = Meal(name=name,
                    description=description,
                    in_diet=in_diet,
                    datetime=current_time,
                    user_id=current_user.id
                    )
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400


@app.route('/meal', methods=['GET'])
def get_meals():

    meals = Meal.query.all()
    meal_list = [meal.to_dict() for meal in meals]

    return jsonify(meal_list)


if __name__ == '__main__':
    app.run(debug=True, port=3333)
