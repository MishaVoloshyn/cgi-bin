from app.models.request import CgiRequest
import io
import json
import sys


class UserController:
    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        action = "do_" + self.request.request_method.lower()
        controller_action = getattr(self, action, None)

        if controller_action:
            controller_action()
        else:
            print("Status: 405 Method Not Allowed")
            print("Content-Type: text/plain; charset=utf-8")
            print()
            print("Method not allowed!")

    def _get_test_data(self):
        return {
            "int": 10,
            "float": 1e-3,
            "str": "Hello",
            "cyr": "Привет"
        }

    def do_get(self):
        data = self._get_test_data()

        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(data, ensure_ascii=False))

    def do_post(self):
        data = self._get_test_data()

        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(data, ensure_ascii=False))
