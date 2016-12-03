from app import db


class Nutrient(db.Model):
    __tablename__ = "nutrient"
    __table_args__ = {'extend_existing': True}
    nut_id = db.Column('nut-id', db.Integer, primary_key=True, autoincrement=False)
    name = db.Column('name', db.VARCHAR(50))
    unit = db.Column('unit', db.VARCHAR(50))
    group = db.Column('group', db.VARCHAR(30))

    def __init__(self, nut_id: int, name: str, unit: str, group: str):
        self.nut_id = nut_id
        self.name = name
        self.unit = unit
        self.group = group


    def __repr__(self):
        return 'nutrient ' + self.name + ' - ' + str(self.nut_id)


    @staticmethod
    def getNutrientsOfFood(ndbno):
        results = db.session.query(Nutrient, FoodHasNutrient).join(FoodHasNutrient, Nutrient.nut_id == FoodHasNutrient.nut_id).filter(
            FoodHasNutrient.food_ndbno == ndbno). \
            filter().all()
        nutsList = []

        for nut, fhn in results:
            nutObj = nut  # type: Nutrient
            fhnObj = fhn  # type: FoodHasNutrient
            nut = {
                "group": nutObj.group,
                "name": nutObj.name,
                "nutrient_id": nutObj.nut_id,
                "unit": nutObj.unit,
                "value": fhnObj.value,
                "id": nutObj.nut_id
            }
            nutsList.append(nut)

        return nutsList

from models.FoodHasNutrient import FoodHasNutrient  # has to be here