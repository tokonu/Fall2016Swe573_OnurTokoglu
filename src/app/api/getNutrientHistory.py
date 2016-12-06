from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify, request
from app.models.UserAteFood import UserAteFood
from app.models.FoodHasNutrient import FoodHasNutrient
from app.models.Nutrient import Nutrient
from app.models.User import User
from datetime import datetime


@app.route('/userarea/getNutrientHistory', methods=['POST'])
@login_required
def getNutrientHistory():
    user = current_user  # type: User
    userId = user.user_id
    recommendedIntake = user.getRecommendedDailyIntake()

    jsonReq = request.get_json()
    print(jsonReq)

    if not jsonReq:
        return jsonify(error="Request error")

    if 'from' not in jsonReq or 'to' not in jsonReq:
        return jsonify(error="Missing values")

    fromStr = jsonReq['from']
    toStr = jsonReq['to']

    # fromStr = "01-01-2016"
    # toStr = "31-12-2016"

    try:
        fromDate = datetime.strptime(fromStr, '%d-%m-%Y')
        toDate = datetime.strptime(toStr, '%d-%m-%Y')
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    results = db.session.query(Nutrient).filter(Nutrient.unit != 'kJ').all()

    nutrients = {}

    for result in results:
        nutObj = result  # type: Nutrient
        nutrients[str(nutObj.nut_id)] = {
            "id": nutObj.nut_id,
            "name": nutObj.name,
            "group": nutObj.group,
            "unit": nutObj.unit,
            "history": [],
            "totalConsumption": 0,
            "numberOfEntries": 0
        }

    results = db.session.query(UserAteFood, FoodHasNutrient).filter(UserAteFood.user_id == userId)\
        .filter(UserAteFood.date >= fromDate).filter(UserAteFood.date <= toDate)\
        .filter(UserAteFood.food_ndbno == FoodHasNutrient.food_ndbno).all()


    for result in results:
        uafObj = result[0]  # type: UserAteFood
        fhnObj = result[1]  # type: FoodHasNutrient
        dateStr = datetime.strftime(uafObj.date, '%d-%m-%Y')
        consumption = fhnObj.value * uafObj.value_g/100
        nut_id = str(fhnObj.nut_id)

        if nut_id not in nutrients:
            continue

        nutrients[nut_id]["totalConsumption"] += consumption
        nutrients[nut_id]["numberOfEntries"] += 1

        histDict = {
            "date": dateStr,
            "consumption": consumption
        }

        for i, hist in enumerate(nutrients[nut_id]["history"]):
            date = datetime.strptime(hist["date"], '%d-%m-%Y').date()
            if date > uafObj.date:
                nutrients[nut_id]["history"].insert(i, histDict)
                break
            elif date == uafObj.date:
                nutrients[nut_id]["history"][i]["consumption"] += consumption
            elif i == len(nutrients[nut_id]["history"]) - 1:
                nutrients[nut_id]["history"].append(histDict)
                break
        if len(nutrients[nut_id]["history"]) == 0:
            nutrients[nut_id]["history"].append(histDict)

    return jsonify(nutrients=nutrients)










