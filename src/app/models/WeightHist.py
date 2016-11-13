from app import db
from models.User import User

class WeightHist(db.Model):
    __tablename__ = "weight_history"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column('user_id',db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    datetime = db.Column('date', db.DateTime(), primary_key=True)
    weight = db.Column('weight', db.Float)
    height = db.Column('height', db.Float)

    def __init__(self, user_id, datetime, weight, height):
        self.user_id = user_id
        self.datetime = datetime
        self.weight = weight
        self.height = height