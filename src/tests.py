import unittest
import json
from app import flask_app as app
from app import db


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




    ## LOGIN RELATED

    def test_index_redirect(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 302, "Index page is not redirected")

    def test_login_page_live(self):
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200, "Server is not running")

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ))

    def logout(self):
        self.app.get('/logout')

    def test_login_fail(self):
        resp = self.login("a@a.com", "aaaaa")
        self.assertIn(b'Wrong email or password', resp.data, "Login didn't fail")

    def test_register_fail(self):
        resp = self.app.post('/register', data=dict(
            email="a@a.com",
            password="aaaaa"
        ))
        self.assertIn(b'Invalid form', resp.data, "Register didn't fail as expected")

    def register(self):
        return self.app.post('/register', data=dict(
            email="a@a.com",
            password="aaaaa",
            name="Onur",
            birthday="11-11-1991",
            weight="88",
            height="188",
            gender="M",
            notes="asd"
        ), follow_redirects=False)

    def test_register_success(self):
        resp = self.register()
        self.assertEqual(resp.status_code, 302, "Not redirecting after register")
        self.assertIn('/userarea', resp.location, "Not redirecting to userarea")

    def test_login_success(self):
        self.register()
        self.logout()
        resp = self.login("a@a.com", "aaaaa")
        self.assertEqual(resp.status_code, 302, "Login not successful or didn't redirect ")
        self.assertIn('/userarea', resp.location, "Not redirecting to userarea")



    ## FOOD RELATED


    def test_search_food_and_add_meal(self):
        self.register()
        data = dict(
            query="cheese"
        )
        resp = self.app.post('userarea/searchFood', data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200, "Search foods status code not 200")
        returnedFoods = json.loads(resp.data.decode('utf-8'))["list"]

        counter = 0
        foods = {}
        for ndbno in returnedFoods:
            food = returnedFoods[ndbno]
            food['nutrients'], food['measures'] = self.get_nutrients_for_food(ndbno)
            food['selectedMeasure'] = food['measures'][0]

            foods[ndbno] = food
            counter += 1
            if counter > 1:
                break

        self.save_food_consumption(foods)


    def get_nutrients_for_food(self, ndbno):
        data = dict(
            ndbno=ndbno
        )
        resp = self.app.post('userarea/getNutrients', data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200, "Search nutrients status code not 200")
        returnedJson = json.loads(resp.data.decode('utf-8'))
        self.assertIn('nutrients', returnedJson, "Search nutrients result doesn't contain nutrients")
        self.assertIn('measures', returnedJson, "Search nutrients result doesn't contain measures")
        nutrients = returnedJson['nutrients']
        measures = returnedJson['measures']
        return nutrients, measures

    def save_food_consumption(self, foods):
        data = dict(
            mealbox=dict(
                foods=foods,
                date="01-01-2016",
                name="meal"
            )
        )
        resp = self.app.post('userarea/saveFoodConsumption', data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200, "Save food consumption status not 200")
        responseStr = resp.data.decode('utf-8')
        self.assertEqual(responseStr, "ok", "Save food consumption failed")



if __name__ == '__main__':
    unittest.main()






















