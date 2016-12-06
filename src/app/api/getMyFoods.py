from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify, request
from app.models.UserAteFood import UserAteFood
from app.models.Food import Food
from datetime import datetime
from sqlalchemy import desc

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


@app.route('/userarea/getMyFoodsForDates', methods=['POST'])
@login_required
def getMyFoodsForDates():
    userId = current_user.user_id

    jsonReq = request.get_json()
    print(jsonReq)

    if not jsonReq:
        return jsonify(error="Request error")

    if 'from' not in jsonReq or 'to' not in jsonReq:
        return jsonify(error="Missing values")

    fromStr = jsonReq['from']
    toStr = jsonReq['to']

    try:
        fromDate = datetime.strptime(fromStr, '%d-%m-%Y')
        toDate = datetime.strptime(toStr, '%d-%m-%Y')
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    results = db.session.query(Food, UserAteFood).filter(UserAteFood.food_ndbno == Food.food_ndbno).filter(UserAteFood.user_id == userId) \
        .filter(UserAteFood.date >= fromDate).filter(UserAteFood.date <= toDate).order_by(desc(UserAteFood.date)).all()

    foodHist = []
    prevDate = ""
    index = -1

    for result in results:
        foodObj = result[0]  # type: Food
        uafObj = result[1]  # type: UserAteFood
        dateStr = datetime.strftime(uafObj.date, '%d-%m-%Y')
        if prevDate != dateStr:
            prevDate = dateStr
            index += 1
            foodHist.append({
                "date": dateStr,
                "foods": []
            })

        measures = foodObj.getMeasures()
        selectedMeasure = measures[0]

        for measure in measures:
            if measure["label"] == uafObj.measure_text:
                selectedMeasure = measure
                selectedMeasure["qty"] = uafObj.measure_value

        foodDict = {
            "name": foodObj.name,
            "ndbno": foodObj.food_ndbno,
            "measures": foodObj.getMeasures(),
            "selectedMeasure": selectedMeasure,
            "entryId": uafObj.id
        }

        foodHist[index]["foods"].append(foodDict)

    return jsonify({"foodHist": foodHist})




@app.route('/userarea/deleteFoodEntry', methods=['POST'])
@login_required
def deleteFoodEntry():

    jsonReq = request.get_json()
    # print(jsonReq)

    if not jsonReq:
        return jsonify(error="Request error")

    if "entryId" not in jsonReq:
        return jsonify(error="Missing values")

    entryId = jsonReq['entryId']

    db.session.query(UserAteFood).filter(UserAteFood.id == entryId).delete()

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(error="Unknown error")

    return "ok"


















