# controllers/order_controller.py
from app.models.request import CgiRequest
import json


class OrderController:
    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        method = self.request.request_method.upper()

        # Поддерживаемые методы
        handlers = {
            "GET":    self.do_get,
            "POST":   self.do_post,
            "PUT":    self.do_put,
            "PATCH":  self.do_patch,
            "DELETE": self.do_delete
        }

        handler = handlers.get(method)
        if handler:
            handler()
        else:
            self._method_not_allowed()

    # GET /order — получить заказы
    def do_get(self):
        data = {
            "api": "order",
            "method": "GET",
            "message": "Получение списка заказов",
            "orders": [
                {"id": 1, "status": "новый", "total": 1500},
                {"id": 2, "status": "в обработке", "total": 3200}
            ]
        }
        self._json_response(data)

    # POST /order — создать заказ
    def do_post(self):
        data = {
            "api": "order",
            "method": "POST",
            "message": "Заказ успешно создан",
            "order_id": 1001,
            "received_data": self.request.query_params
        }
        self._json_response(data, status="201 Created")

    # PUT /order — полная замена заказа
    def do_put(self):
        data = {
            "api": "order",
            "method": "PUT",
            "message": "Заказ полностью обновлён",
            "order_id": 1001
        }
        self._json_response(data)

    # PATCH /order — частичное обновление
    def do_patch(self):
        data = {
            "api": "order",
            "method": "PATCH",
            "message": "Заказ частично обновлён (например, статус)",
            "updated_fields": ["status"]
        }
        self._json_response(data)

    # DELETE /order — удаление заказа
    def do_delete(self):
        data = {
            "api": "order",
            "method": "DELETE",
            "message": "Заказ успешно удалён",
            "order_id": 1001
        }
        self._json_response(data)

    def _json_response(self, data, status="200 OK"):
        print(f"Status: {status}")
        print("Content-Type: application/json; charset=utf-8")
        print()

        print(json.dumps(data, ensure_ascii=False, indent=2))

    def _method_not_allowed(self):
        print("Status: 405 Method Not Allowed")
        print("Content-Type: application/json; charset=utf-8")
        print()
        
        print(json.dumps({
            "error": "Method Not Allowed",
            "api": "order",
            "allowed": ["GET", "POST", "PUT", "PATCH", "DELETE"]
        }, ensure_ascii=False, indent=2))