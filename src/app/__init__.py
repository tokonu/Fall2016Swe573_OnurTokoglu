from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


flask_app = Flask(__name__)
flask_app.config.from_object('config')

db = SQLAlchemy(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)

# Models must be imported after db variable init and before create_all call
# db.create_all() function creates necessary tables if they don't exist


import app.login
import app.api

import app.models

db.create_all()
db.session.commit()

print("creating activity table")

with open("activity.sql", "r") as act:
    for line in act:
        try:
            db.session.execute(line)
        except:
            pass
    db.session.commit()
