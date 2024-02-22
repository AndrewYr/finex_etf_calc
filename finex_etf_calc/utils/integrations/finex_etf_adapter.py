import os
import datetime
from httpx import AsyncClient

from finex_etf_calc.utils.integrations.handlers import async_handle_http_errors


class FinexAdapter:
    def __init__(self):
        self.client = AsyncClient

    @classmethod
    def check_date_file_today(cls, path_to_file: str) -> bool:
        try:
            mtime = os.path.getmtime(path_to_file)
            if datetime.date.fromtimestamp(mtime) == datetime.date.today():
                return True
        except FileNotFoundError:
            pass  # TODO добавить информативный лог
        return False

    @async_handle_http_errors
    async def send_request(self, url: str):
        async with self.client() as client:
            return await client.get(url)

    async def load_file_from_url(self, url: str, path_to_file: str):
        if not self.check_date_file_today(path_to_file):
            with open(path_to_file, "wb") as f:
                response = await self.send_request(url)
                f.write(response.content)
