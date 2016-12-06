from app import flask_app as app
from flask_login import login_required, current_user
from flask import jsonify
from app.models.Nutrient import Nutrient


@app.route('/userarea/getNutrientsFromLocal/<ndbno>', methods=['POST', 'GET'])
@login_required
def getNutrientsFromLocal(ndbno):

    # results = db.session.query(Nutrient, FoodHasNutrient).join(FoodHasNutrient).filter(FoodHasNutrient.food_ndbno == ndbno).\
    #     filter().all()
    # nutsList = []
    #
    # for nut,fhn in results:
    #     nutObj = nut  # type: Nutrient
    #     fhnObj = fhn  # type: FoodHasNutrient
    #     nut = {
    #         "group": nutObj.group,
    #         "name": nutObj.name,
    #         "nutrient_id": nutObj.nut_id,
    #         "unit": nutObj.unit,
    #         "value": fhnObj.value
    #     }
    #     nutsList.append(nut)

    nutsList = Nutrient.getNutrientsOfFood(ndbno)
    print("returned nutrients " + str(len(nutsList)))
    return jsonify({"nutrients":nutsList})


def hello():
    print('hello');