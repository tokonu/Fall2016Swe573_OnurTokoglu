from app import flask_app as app
from flask_login import login_required
from flask import request
from flask import jsonify
from .FCD import FCD


@app.route('/userarea/getNutrients', methods=['POST'])
@login_required
def getNutrients():
    ndbno = request.get_json()['ndbno']
    if not ndbno or ndbno == "":
        return jsonify(error="Food no error")

    nutrientList = []
    nutrientJsons = FCD.get_nutrients(ndbno)

    for nutrientJson in nutrientJsons:
        nutrient = {};
        nutrient['name'] = nutrientJson['name']
        nutrient['nutrient_id'] = nutrientJson['nutrient_id']
        nutrient['unit'] = nutrientJson['unit']
        nutrient['value'] = nutrientJson['value']
        nutrient['group'] = nutrientJson['group']
        nutrientList.append(nutrient)

    measureGram = {
        'label' : 'g',
        'eqv' : 1,
        'qty' : 100
    }
    measures = [measureGram]

    for measure in nutrientJsons[0]['measures']:
        if measure['label'] == 'g':
            continue
        del measure['value']
        if int(measure['qty']) != 1:
            measure['eqv'] = float(measure['eqv'])/float(measure['qty'])
        measures.append(measure);

    #measures = nutrientJsons[0]['measures']

    return jsonify(ndbno=ndbno, measures=measures, nutrients=nutrientList)