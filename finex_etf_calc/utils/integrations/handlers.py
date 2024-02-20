from functools import wraps
from httpx import RequestError, HTTPStatusError


def handle_http_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return response
        except HTTPStatusError as e:
            # Обработка случаев, когда сервер возвращает код ошибки (например, 400, 500)
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            # Можно выбросить исключение или вернуть значение по умолчанию
            raise
        except RequestError as e:
            # Обработка ошибок соединения (например, проблемы с сетью)
            print(f"Request error occurred: {e}")
            raise
        except Exception as e:
            # Обработка остальных исключений
            print(f"An error occurred: {e}")
            raise
    return wrapper


def async_handle_http_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as e:
            if 400 <= e.response.status_code < 500:
                # Обработка клиентских ошибок
                print(f"Client error occurred: {e.response.status_code} - {e.response.text}")
            elif 500 <= e.response.status_code < 600:
                # Обработка серверных ошибок
                print(f"Server error occurred: {e.response.status_code} - {e.response.text}")
            else:
                # Обработка всех остальных HTTP ошибок
                print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            # Перебрасываем исключение после обработки или обработайте его как необходимо
            raise
    return wrapper
