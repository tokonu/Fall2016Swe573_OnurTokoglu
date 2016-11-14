from app import db
from .User import User


class Recipe(db.Model):
    __tablename__ = "recipe"
    __table_args__ = {'extend_existing': True}
    recipe_id = db.Column("recipe-id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user-id', db.Integer, db.ForeignKey(User.user_id))
    name = db.Column('name', db.VARCHAR(30))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name