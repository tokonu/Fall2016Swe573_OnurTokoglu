from app import db
from models.Food import Food
from models.Nutrient import Nutrient

class FoodHasNutrient(db.Model):
    __tablename__ = "food_has_nutrient"
    __table_args__ = {'extend_existing': True}
    food_ndbno = db.Column('food-ndbno', db.VARCHAR(20), db.ForeignKey(Food.food_ndbno), primary_key=True)
    nut_id = db.Column('nut-id', db.Integer, db.ForeignKey(Nutrient.nut_id), primary_key=True)
    value = db.Column('value', db.Float)

    def __init__(self, food_ndbno: str, nut_id: int, value: float):
        self.food_ndbno = food_ndbno
        self.nut_id = nut_id
        self.value = value
