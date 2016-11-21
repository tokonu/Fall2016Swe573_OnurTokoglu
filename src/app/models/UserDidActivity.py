from app import db
from .Activity import Activity
from .User import User


class UserDidActivity(db.Model):
    __tablename__ = "user_did_activity"
    __table_args__ = {'extend_existing': True}
    id = db.Column("id",db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column('activity-id', db.Integer, db.ForeignKey(Activity.id))
    user_id = db.Column('user-id', db.Integer, db.ForeignKey(User.user_id))
    date = db.Column('date', db.Date)
    kcal = db.Column('kcal', db.Float)
    duration_mnt = db.Column('duration-mnt', db.Float)

    def __init__(self, activity_id, user_id, date, kcal, duration_mnt):
        self.activity_id = activity_id
        self.user_id = user_id
        self.date = date
        self.kcal = kcal
        self.duration_mnt = duration_mnt