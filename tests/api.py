
from alphaz.utils.api import api
from alphaz.models.tests import Test
import requests, os

from alphaz.utils.api import api

class API_tests(Test):
    def __init__(self):
        print(os.getcwd())
        api.init(config_path='api')
        super().__init__()

    def get_url(self,route):
        url         = api.get_url() + route
        return url

    def post(self,data,route):
        try:
            response    = requests.post(self.get_url(route), data=data)
            return str(response.text)
        except Exception as ex:
            print("ERROR",ex)
            return None

    def get(self,data,route):
        try:
            response    = requests.get(self.get_url(route), params=data)
            return str(response.text)
        except Exception as ex:
            print("ERROR",ex)
            return None

    def test_api_up(self):
        key         = "testing"
        data        = {"name": key }
        response    = self.get(data=data,route='/test')
        return response is not None and key in response