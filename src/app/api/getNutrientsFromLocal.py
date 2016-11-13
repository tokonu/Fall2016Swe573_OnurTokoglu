from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify
from models.Nutrient import Nutrient
from models.FoodHasNutrient import FoodHasNutrient


@app.route('/userarea/getNutrientsFromLocal/<ndbno>', methods=['POST', 'GET'])
@login_required
def getNutrientsFromLocal(ndbno):

    results = db.session.query(Nutrient, FoodHasNutrient).join(FoodHasNutrient).filter(FoodHasNutrient.food_ndbno == ndbno).\
        filter().all()
    nutsList = []

    for nut,fhn in results:
        nutObj = nut  # type: Nutrient
        fhnObj = fhn  # type: FoodHasNutrient
        nut = {
            "group": nutObj.group,
            "name": nutObj.name,
            "nutrient_id": nutObj.nut_id,
            "unit": nutObj.unit,
            "value": fhnObj.value
        }
        nutsList.append(nut)
    print("returned nutrients " + str(len(nutsList)))
    return jsonify({"nutrients":nutsList})