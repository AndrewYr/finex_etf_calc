import os
import datetime
from httpx import AsyncClient, Client


class FinexAdapter:
    def __init__(self):
        self.client = AsyncClient()

    @classmethod
    def check_date_file_today(cls, path_to_file: str) -> bool:
        try:
            mtime = os.path.getmtime(path_to_file)
            if datetime.date.fromtimestamp(mtime) == datetime.date.today():
                return True
        except FileNotFoundError:
            pass  # TODO добавить информативный лог
        return False

    async def load_file_from_url(self, url: str, path_to_file: str):
        if not self.check_date_file_today(path_to_file):
            async with self.client as client:
                with open(path_to_file, "wb") as f:
                    response = await client.get(url)
                    f.write(response.content)


class CBRAdapter:
    def __init__(self):
        self.client = Client()

    @staticmethod
    def body():
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetCursDynamicXML xmlns="http://web.cbr.ru/">
      <FromDate>2023-01-01</FromDate>
      <ToDate>2023-01-02</ToDate>
      <ValutaCode>840</ValutaCode>
    </GetCursDynamicXML>
  </soap12:Body>
</soap12:Envelope>'''

    def get_actual_price_currency(self):
        req_body = self.body()
        resp = self.client.post(
            'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx',
            headers={
                'content-type': 'text/xml',
            },
            content='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCursOnDate xmlns="http://web.cbr.ru/">
      <On_date>2023-12-24</On_date>
    </GetCursOnDate>
  </soap:Body>
</soap:Envelope>''')
        a = 0


r = CBRAdapter()
r.get_actual_price_currency()
