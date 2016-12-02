from app import db
from app.login.RegisterForm import RegisterForm
from datetime import date

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column('user-id', db.Integer, primary_key=True)
    email = db.Column('email', db.VARCHAR(40), unique=True, index=True)
    password = db.Column('password', db.VARCHAR(100))
    name = db.Column('name', db.VARCHAR(50))
    birthday = db.Column('birthday', db.Date())
    height = db.Column('height', db.Float)
    weight = db.Column('weight', db.Float)
    gender = db.Column('gender', db.Enum('M', 'F'))
    notes = db.Column('notes', db.VARCHAR(300))

    def __init__(self, form: RegisterForm):
        self.email = form.email
        self.password = form.password
        self.name = form.name
        self.birthday = form.birthday
        self.height = form.height
        self.weight = form.weight
        self.gender = form.gender
        self.notes = form.notes


    def getRecommendedDailyIntake(self):
        recommended = 0
        if self.gender == 'M':
            recommended = 1.2 * (5 + self.weight*10 + self.height*6.25 - self.getAge()*5)
        else:
            recommended = 1.2 * (-161 + self.weight*10 + self.height*6.25 + self.getAge()*5)
        return round(recommended)

    def getAge(self):
        born = self.birthday
        today = date.today()
        years_difference = today.year - born.year
        is_before_birthday = (today.month, today.day) < (born.month, born.day)
        elapsed_years = years_difference - int(is_before_birthday)
        return elapsed_years

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User %r>' % self.email