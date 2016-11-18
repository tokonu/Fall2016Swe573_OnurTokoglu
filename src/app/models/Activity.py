from app import db


class Activity(db.Model):
    __tablename__ = "activity"
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(64))
    kcal_ph_pkg = db.Column('kcal_ph_pkg', db.Float)

    def __init__(self, id, name, kcal_ph_pkg):
        self.id = id
        self.name = name
        self.kcal_ph_pkg = kcal_ph_pkg

    def __repr__(self):
        return 'food' + self.food_ndbno + ' - ' + self.name