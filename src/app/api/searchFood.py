from app import flask_app as app
from flask_login import login_required
from flask import request
from flask import jsonify
from .FCD import FCD


@app.route('/userarea/searchFood', methods=['POST'])
@login_required
def searchFood():
    queryString = request.get_json()['query']
    if not queryString or len(queryString) < 4:
        return jsonify(error="Enter valid string")

    foodList = {};
    foodJsons = FCD.find(queryString)

    for foodJson in foodJsons:
        ndbno = foodJson['ndbno']
        food = {};
        food['name'] = foodJson['name']
        food['ndbno'] = ndbno
        foodList[ndbno] = food

    return jsonify(**dict(list=foodList))

