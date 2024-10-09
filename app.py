import binascii
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
login_manager = LoginManager()

if READY_TO_RUN:
    app.config['SECRET_KEY'] = CONFIG_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG_DATABASE_URI

    db.init_app(app)
    migrate = Migrate(app, db)
else:
    sys.exit()

login_manager.login_view = 'login'


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
        print(byte_value)
        if user and bcrypt.checkpw(str.encode(password), byte_value):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/user', methods=['POST'])
def create_user():
    return jsonify({"message": "Dados inválidos"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=3333)
