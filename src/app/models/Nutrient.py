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
