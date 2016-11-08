from app import flask_app as app
from flask_login import login_required, current_user
from flask import request
from flask import jsonify
from .FCD import FCD


@app.route('/userarea/searchFood', methods=['POST'])
@login_required
def searchFood():
    queryString = request.get_json()['query']
    if not queryString or len(queryString) < 4:
        return jsonify(error="Enter valid string")

    foodArray = [];
    foodJsons = FCD.find(queryString)

    for foodJson in foodJsons:
        food = {};
        food['name'] = foodJson['name']
        food['ndbno'] = foodJson['ndbno']
        foodArray.append(food)

    return jsonify(**dict(list=foodArray))

