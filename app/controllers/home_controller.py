from app.models.request import CgiRequest



class HomeController:
    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        # parts[0] — язык, parts[1] — контроллер, parts[2] — действие
        action_name = (
            self.request.path_parts[2].lower()
            if len(self.request.path_parts) > 2 and self.request.path_parts[2].strip()
            else 'index'
        )

        if not hasattr(self, action_name):
            self._not_found()
            return

        action = getattr(self, action_name)
        action()

    # ------------------------------------------------------------------
    # Главная страница - ссылки
    # ------------------------------------------------------------------
    def index(self):
        html = f'''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>CGI Py — Главная</title>
            <link rel="stylesheet" href="/css/site.css" />
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ margin: 15px 0; }}
                h1 {{ font-size: 1.5em }}
                a {{ font-size: 1.1em; text-decoration: none; color: #0066cc; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>Добро пожаловать в CGI-приложение на Python</h1>
            <ul>
                <li><a href="/uk-UA/home/params?htctrl=1">Параметры окружения, заголовки и GET-параметры</a></li>
                <li><a href="/uk-UA/home/do_get?htctrl=1">Тестовый метод do_get</a></li>
                <li><a href="/uk-UA/usertest?htctrl=1">Тестовый контроллер Usertest</a></li>
                <li><a href="/uk-UA/user?htctrl=1">UserController (GET)</a></li>
            </ul>
            <p><img src="/img/icon.png" width="120" alt="icon"></p>
        </body>
        </html>
        '''

        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)

    # ------------------------------------------------------------------
    # Отображение всех параметров
    # ------------------------------------------------------------------
    def params(self):
        envs = ""
        for key, value in sorted(self.request.server.items(), key=lambda x: x[0].lower()):
            envs += f"<tr><td>{key}</td><td>{value}</td></tr>\n"

        hdrs = ""
        for key, value in sorted(self.request.headers.items(), key=lambda x: x[0].lower()):
            hdrs += f"<tr><td>{key}</td><td>{value}</td></tr>\n"

        qp = ""
        for key, value in sorted(self.request.query_params.items(), key=lambda x: x[0].lower()):
            qp += f"<tr><td>{key}</td><td>{value}</td></tr>\n"

        html = f'''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>CGI Py — Параметры</title>
            <link rel="stylesheet" href="/css/site.css" />
            <style>
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #555; padding: 6px 10px; text-align: left; }}
                th {{ background-color: #f0f0f0; }}
                h1, h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Все параметры запроса</h1>
            <p><a href="/uk-UA/home?htctrl=1">← На главную</a></p>

            <h2>Переменные окружения (os.environ)</h2>
            <table>{envs}</table>

            <h2>HTTP-заголовки</h2>
            <table>{hdrs}</table>

            <h2>GET-параметры (query string)</h2>
            <table>{qp}</table>

            <p>
                <img src="/img/icon.png" width="100" alt="icon">
                <img src="/img/m13.jpg" width="100" alt="m13">
            </p>
        </body>
        </html>
        '''

        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)

    # ------------------------------------------------------------------
    # Простой тестовый метод
    # ------------------------------------------------------------------
    def do_get(self):
        print("Content-Type: text/plain; charset=utf-8")
        print()
        print("HomeController::do_get — всё работает!")

    # ------------------------------------------------------------------
    # 404-страница для неизвестных действий
    # ------------------------------------------------------------------
    def _not_found(self):
        print("Status: 404 Not Found")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(f'''
        <!DOCTYPE html>
        <html lang="ru">
        <head><meta charset="UTF-8"><title>404</title></head>
        <body>
            <h1>404 — Действие не найдено</h1>
            <p>Запрошенное действие <strong>{self.request.path_parts[2] if len(self.request.path_parts) > 2 else ""}</strong> отсутствует.</p>
            <p><a href="/uk-UA/home?htctrl=1">&#8592; На главную</a></p>
        </body>
        </html>
        ''')
