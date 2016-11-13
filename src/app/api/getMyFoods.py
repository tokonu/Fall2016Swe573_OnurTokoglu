from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify
from models.UserAteFood import UserAteFood
from models.Food import Food


@app.route('/userarea/getMyFoods', methods=['POST'])
@login_required
def getMyFoods():
    userId = current_user.user_id

    results = db.session.query(Food).join(UserAteFood).filter(UserAteFood.user_id == userId).all()

    foodsDict = {}

    for result in results:
        foodObj = result  # type: Food
        foodsDict[foodObj.food_ndbno] = {
            "name": foodObj.name,
            "ndbno": foodObj.food_ndbno,
            "measures": foodObj.getMeasures()
        }


    print("returned myfoods " +str(len(foodsDict)))
    return jsonify({"foods":foodsDict})

