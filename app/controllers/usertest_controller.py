# controllers/usertest_controller.py
from app.models.request import CgiRequest


class UsertestController:
    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        action = (
            self.request.path_parts[2].lower()
            if len(self.request.path_parts) > 2 and self.request.path_parts[2].strip()
            else 'index'
        )
        method = getattr(self, action, None)
        if method is None:
            self._not_found()
            return
        method()

    def index(self):
        try:
            with open("./views/_layout.html", "r", encoding="utf-8") as f:
                layout = f.read()
            with open("./views/usertest_index.html", "r", encoding="utf-8") as f:
                body = f.read()
        except FileNotFoundError as e:
            print("Content-Type: text/html; charset=utf-8")
            print()
            print(f"<h1>Ошибка: {e}</h1>")
            return

        print("Content-Type: text/html; charset=utf-8")
        print()
        print(layout.replace("<!-- RenderBody -->", body))

    def _not_found(self):
        print("Status: 404 Not Found")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<h1>404 — Действие не найдено</h1>")
