from datetime import datetime as _datetime
from database import db


class Meal(db.Model):
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=_datetime.utcnow)
    in_diet = db.Column(db.Boolean(), nullable=False)

    def __init__(self, name, description, datetime, in_diet) -> None:
        self.name = name
        self.description = description
        self.datetime = datetime
        self.in_diet = in_diet

    def __repr__(self):
        return f"<Meal {self.name}>"
