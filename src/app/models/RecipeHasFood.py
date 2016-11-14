from app import db
from .Food import Food
from .Recipe import Recipe

class RecipeHasFood(db.Model):
    __tablename__ = "recipe_has_food"
    __table_args__ = {'extend_existing': True}
    recipe_id = db.Column('recipe-id', db.Integer, db.ForeignKey(Recipe.recipe_id), primary_key=True)
    food_ndbno = db.Column('food-ndbno', db.VARCHAR(20), db.ForeignKey(Food.food_ndbno), primary_key=True)
    value_g = db.Column('value-g', db.Float)
    measure_value = db.Column('measure-value', db.Float)
    measure_text = db.Column('measure-text', db.VARCHAR(30))

    def __init__(self, recipe_id, food_ndbno, value_g, measure_value, measure_text):
        self.recipe_id = recipe_id
        self.food_ndbno = food_ndbno
        self.value_g = value_g
        self.measure_value = measure_value
        self.measure_text = measure_text