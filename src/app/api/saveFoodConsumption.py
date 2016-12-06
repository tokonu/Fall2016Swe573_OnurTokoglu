from app import flask_app as app
from app import db
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from app.models.Food import Food
from app.models.Nutrient import Nutrient
from app.models.FoodHasNutrient import FoodHasNutrient
from app.models.UserAteFood import UserAteFood
from app.models.RecipeHasFood import RecipeHasFood
from datetime import datetime
from app.models.Recipe import Recipe

@app.route('/userarea/saveFoodConsumption', methods=['POST'])
@login_required
def saveFoodConsumption():
    mealbox = request.get_json()['mealbox']
    if not mealbox or 'foods' not in mealbox or 'date' not in mealbox:
        return jsonify(error="Missing values in request")

    try:
        date = datetime.strptime(mealbox['date'], '%d-%m-%Y')
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    foods = mealbox['foods']
    userId = current_user.user_id

    if 'name' in mealbox:
        recipeName = mealbox['name']
        recipe = Recipe(user_id=userId,name=recipeName)

        try:
            db.session.add(recipe)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(error="Try again later")

    for ndbno, foodDict in foods.items():
        if 'nutrients' not in foodDict or 'measures' not in foodDict or 'ndbno' not in foodDict \
                or 'selectedMeasure' not in foodDict:
            print('fooddict missing values')
            continue

        selectedMeasure = foodDict['selectedMeasure']
        if 'label' not in selectedMeasure or 'qty' not in selectedMeasure or 'eqv' not in selectedMeasure:
            return jsonify(error="Enter valid input")

        measureText = selectedMeasure['label']
        try:
            measureValue = float(selectedMeasure['qty'])
            measureEqv = float(selectedMeasure['eqv'])  # equivalent to 100g
        except:
            print("return")
            return jsonify(error="Enter valid input")

        if measureValue <= 0 or measureEqv <= 0:
            return jsonify(error="Enter valid input")


        foodObj = getFoodObjectFromDict(foodDict)
        if not foodObj:
            print("saveFoodConsumption no foodobj")
            continue
        saveFoodToDb(foodObj, foodDict)

        kcal = getEnergyOfFood(foodDict['nutrients'], measureEqv, measureValue)

        uaf = UserAteFood(foodObj.food_ndbno, userId, date, kcal, measureEqv*measureValue, measureValue, measureText)

        try:
            db.session.add(uaf)
            db.session.commit()
        except:
            db.session.rollback()

        try:
            rhf = RecipeHasFood(recipe_id=recipe.recipe_id, food_ndbno=foodObj.food_ndbno,
                                value_g=measureValue*measureEqv, measure_value=measureValue, measure_text=measureText)
            db.session.add(rhf)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    return "ok"

def getFoodObjectFromDict(foodDict):
    try:
        ndbno = foodDict['ndbno']
        name = foodDict['name']
        measures = foodDict['measures']
    except:
        return

    return Food(ndbno, name, measures)



def getNutrientObjectFromDict(nutrientDict):
    try:
        nut_id = nutrientDict['nutrient_id']
        name = nutrientDict['name']
        unit = nutrientDict['unit']
        group = nutrientDict['group']
    except:
        return

    return Nutrient(nut_id, name, unit, group)



def getEnergyOfFood(nutrientsDict, measureEqv, measureVal):
    for nutDict in nutrientsDict:
        if nutDict['name'] == 'Energy' and nutDict['unit'] == 'kcal':
            nutrientValue = float(nutDict['value']) #per 100 gram
            return nutrientValue*measureVal*measureEqv/100




def saveFoodToDb(foodObj, foodDict):
    try:
        db.session.add(foodObj)
        db.session.commit()
    except:
        db.session.rollback()
        print("saveFoodToDb food exists")
        return
    saveNutrientsToDb(foodDict)



def saveNutrientsToDb(foodDict):
    print("saving nutrients")
    food_ndbno = foodDict['ndbno']
    for nutrientDict in foodDict['nutrients']:
        nutObj = getNutrientObjectFromDict(nutrientDict)
        try:
            db.session.add(nutObj)
            db.session.commit()
        except:
            db.session.rollback()

        value = float(nutrientDict['value'])

        fhn = FoodHasNutrient(food_ndbno, nutObj.nut_id, value)

        try:
            db.session.add(fhn)
            db.session.commit()
        except:
            db.session.rollback()










