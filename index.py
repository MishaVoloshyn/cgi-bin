#!C:/python/python.exe
# -*- coding: utf-8 -*-

import os
import sys
from urllib.parse import parse_qs

# Делаем вывод в UTF-8, чтобы русские буквы не были "????"
sys.stdout.reconfigure(encoding="utf-8")

# Путь к корню твоего приложения (где лежит папка app)
APP_ROOT = r"C:\xampp\cgi-bin"



# Добавляем APP_ROOT в sys.path, чтобы работал импорт "from app...."
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

# Делаем рабочей директорией папку app, чтобы ./views искался правильно
os.chdir(os.path.join(APP_ROOT, "app"))

from app.models.request import CgiRequest
from app.controllers.home_controller import HomeController
from app.controllers.ordertest_controller import OrdertestController
from app.controllers.order_controller import OrderController
from app.controllers.user_controller import UserController
from app.controllers.usertest_controller import UsertestController


def main():
    # Всё, что дал Apache (REQUEST_METHOD, PATH_INFO и т.д.)
    server = dict(os.environ)

    # Разбираем query string → query_params
    query_string = os.environ.get("QUERY_STRING", "")
    raw_qs = parse_qs(query_string, keep_blank_values=True)
    query_params = {k: (v[0] if len(v) == 1 else v) for k, v in raw_qs.items()}

    # Собираем заголовки из HTTP_*
    headers = {}
    for key, value in os.environ.items():
        if key.startswith("HTTP_"):
            name = key[5:].replace("_", "-").title()
            headers[name] = value

    # PATH_INFO вида /uk-UA/order или /uk-UA/home/params
    path = os.environ.get("PATH_INFO", "/uk-UA/home")
    path_parts = [p for p in path.split("/") if p]

    lang = path_parts[0] if len(path_parts) > 0 else "uk-UA"
    controller_name = path_parts[1].lower() if len(path_parts) > 1 else "home"

    # Создаём наш CgiRequest
    req = CgiRequest(
        server=server,
        query_params=query_params,
        headers=headers,
        path=path,
        controller=controller_name,
        path_parts=path_parts,
    )

    # Роутинг контроллеров
    controllers = {
        "home": HomeController,
        "ordertest": OrdertestController,
        "order": OrderController,
        "user": UserController,
        "usertest": UsertestController,
    }

    controller_cls = controllers.get(controller_name, HomeController)
    controller = controller_cls(req)
    controller.serve()


if __name__ == "__main__":
    main()
