from app import db
from json import dumps,loads


class Food(db.Model):
    __tablename__ = "food"
    __table_args__ = {'extend_existing': True}
    food_ndbno = db.Column('food-ndbno', db.VARCHAR(20), primary_key=True)
    name = db.Column('name', db.VARCHAR(150))
    measuresString = db.Column('measures', db.Text)

    def __init__(self, ndbno, name, measures):
        self.food_ndbno = ndbno
        self.name = name
        if 'qty' in measures:
            del measures['qty']
        self.measuresString = dumps(measures)

    def getMeasures(self):
        return loads(self.measuresString)


    def __repr__(self):
        return 'food' + self.food_ndbno + ' - ' + self.name