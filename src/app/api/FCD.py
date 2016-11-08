import requests


class FCD():
    API_URL = "http://api.nal.usda.gov/ndb/{}/?format=json&api_key=hEnX0mhdBvaCN0UV0CIJOEi3p2uBv5rHwx4QDqiY"

    @staticmethod
    def get_url(command):
        return FCD.API_URL.format(command)

    @staticmethod
    def find(name):
        base_url = FCD.get_url("search")
        url = base_url + "&q={}".format(name)
        json_response = requests.get(url).json()
        if "list" not in json_response:
            return []
        list = json_response["list"]["item"]
        return list

    @staticmethod
    def get_report(ndbno):
        base_url = FCD.get_url("reports")
        url = base_url + "&type=f&ndbno={}".format(ndbno)
        json_response = requests.get(url).json()["report"]
        return json_response

    @staticmethod
    def get_nutrients(ndbno):
        report = FCD.get_report(ndbno)
        return report["food"]["nutrients"]
