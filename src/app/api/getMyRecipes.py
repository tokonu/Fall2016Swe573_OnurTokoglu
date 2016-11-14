from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify
from models.Recipe import Recipe
from models.Food import Food
from models.RecipeHasFood import RecipeHasFood
from models.Nutrient import Nutrient
import json

@app.route('/userarea/getMyRecipes', methods=['POST'])
@login_required
def getMyRecipes():
    userId = current_user.user_id

    results = db.session.query(Recipe).filter(Recipe.user_id == userId).all()

    recipeDict = {}

    for result in results:
        recipeObj = result  # type: Recipe
        recipeDict[recipeObj.recipe_id] = {
            'id': recipeObj.recipe_id,
            'name':recipeObj.name
        }


    print("returned myrecipes " +str(len(recipeDict)))
    return jsonify({"recipes":recipeDict})


@app.route('/userarea/getFoodsInRecipe/<recipeId>', methods=['POST','GET'])
@login_required
def getFoodsInRecipe(recipeId):

    results = db.session.query(Food, RecipeHasFood).join(RecipeHasFood).filter(RecipeHasFood.recipe_id == recipeId).all()
    foodsDict = {}

    for food, rhf in results:
        foodObj = food  # type: Food
        rhfObj = rhf  # type: RecipeHasFood
        measures = foodObj.getMeasures()

        selectedMeasure = measures[0]
        for measure in measures:
            if measure['label'] == rhfObj.measure_text:
                selectedMeasure = measure
                selectedMeasure['qty'] = rhfObj.measure_value

        nutrients = Nutrient.getNutrientsOfFood(foodObj.food_ndbno)

        foodDict = {
            'ndbno': foodObj.food_ndbno,
            'name': foodObj.name,
            'measures': measures,
            'value_g': rhfObj.value_g,
            'measure_text': rhfObj.measure_text,
            'measure_value': rhfObj.measure_value,
            'nutrients': nutrients,
            'selectedMeasure': selectedMeasure
        }

        foodsDict[foodObj.food_ndbno] = foodDict

    print("getfoodsinrecipes returned " + str(len(foodsDict)))
    return jsonify({"foods":foodsDict})







