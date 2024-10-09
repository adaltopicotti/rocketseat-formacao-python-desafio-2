from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.Text(), nullable=False, default='user')

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"
