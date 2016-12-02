from app import db
from .Food import Food
from .User import User


class UserAteFood(db.Model):
    __tablename__ = "user_ate_food"
    __table_args__ = {'extend_existing': True}
    id = db.Column("id",db.Integer, primary_key=True, autoincrement=True)
    food_ndbno = db.Column('food-ndbno', db.VARCHAR(20), db.ForeignKey(Food.food_ndbno))
    user_id = db.Column('user-id', db.Integer, db.ForeignKey(User.user_id))
    date = db.Column('date', db.Date)
    kcal = db.Column('kcal', db.Float)
    value_g = db.Column('value-g', db.Float)
    measure_value = db.Column('measure-value', db.Float)
    measure_text = db.Column('measure-text', db.VARCHAR(30))

    def __init__(self, food_ndbno, user_id, date, kcal, value_g, measure_value, measure_text):
        self.food_ndbno = food_ndbno
        self.user_id = user_id
        self.date = date
        self.kcal = kcal
        self.value_g = value_g
        self.measure_value = measure_value
        self.measure_text = measure_text

    def __repr__(self):
        return "User ate food " + self.food_ndbno