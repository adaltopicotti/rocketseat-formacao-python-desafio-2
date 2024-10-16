from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.Text(), nullable=False, default='user')

    meals = db.relationship('Meal', back_populates='user', lazy=True)

    def __init__(self, username, password, role) -> None:
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.username}>"
