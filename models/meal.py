from datetime import datetime as _datetime
from database import db


class Meal(db.Model):
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=_datetime.utcnow)
    in_diet = db.Column(db.Boolean(), nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='meals')

    def __init__(self, name, description, datetime, in_diet, user_id) -> None:
        self.name = name
        self.description = description
        self.datetime = datetime
        self.in_diet = in_diet
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'datetime': self.datetime.isoformat(),
            'in_diet': self.in_diet,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f"<Meal {self.name}>"
