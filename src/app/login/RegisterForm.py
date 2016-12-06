import re
from datetime import datetime

class RegisterForm():
    def __init__(self, form):
        self.email = form['email']
        self.password = form['password']
        self.name = form['name']
        self.birthday = form['birthday']
        self.height = form['height']
        self.weight = form['weight']
        self.gender = form['gender']
        self.notes = form['notes']

    @property
    def validate(self) -> str:
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email) is None:
            return "Invalid email"

        if len(self.password) < 5:
            return "Password less than 5 characters"

        if self.name is None or self.name == "":
            return "Enter Name"

        if self.birthday is None:
            return "Enter Birthday"
        else:
            try:
                dateobj = datetime.strptime(self.birthday,'%d-%m-%Y')
            except Exception as e:
                print("date conversion error ")
                print(e)
                return "Enter birthday in DD-MM-YYYY format"

        if self.height is None or self.height == "":
            return "Enter height"
        else:
            try:
                height_float = float(self.height)
                if 30 < height_float < 300:
                    self.height = int(height_float*10)/10.0
                else:
                    return "Height invalid. Enter your height in cm"
            except:
                return "Height invalid"

        if self.weight is None or self.weight == "":
            return "Enter weight"
        else:
            try:
                weight_float = float(self.weight)
                if 30 < weight_float < 300:
                    self.weight = int(weight_float*10)/10.0
                else:
                    "Weight invalid. Enter your weight in kg"
            except:
                return "Weight invalid"

        if not (self.gender == 'M' or self.gender == 'F'):
            return "Gender invalid"

        if len(self.notes) > 300:
            return "Notes more than 300 chars"

        return None