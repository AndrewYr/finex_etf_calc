import typing as t
import datetime
import xml.etree.ElementTree as ET
from datetime import date

from httpx import Client, Response

from finex_etf_calc.app.config import config
from finex_etf_calc.utils.integrations.handlers import handle_http_errors


class CBRAdapter:
    def __init__(self):
        self.client = Client()

    @staticmethod
    def _xml_to_list(xml_str: str, findall_text) -> t.List[dict]:
        root = ET.fromstring(xml_str)
        valute_curs_dynamic_elements = root.findall(f".//{findall_text}")
        response_list = []
        for valute_curs_dynamic in valute_curs_dynamic_elements:
            response_list.append({
                'VchCode': valute_curs_dynamic.findtext("VchCode"),
                'CursDate': valute_curs_dynamic.findtext("CursDate"),
                'Vcode': valute_curs_dynamic.findtext("Vcode"),
                'Vnom': valute_curs_dynamic.findtext("Vnom"),
                'Vcurs': valute_curs_dynamic.findtext("Vcurs"),
                'VunitRate': valute_curs_dynamic.findtext("VunitRate")
            })
        return response_list

    @staticmethod
    def _get_on_date_value(xml_string):

        root = ET.fromstring(xml_string)
        namespaces = {
            'xs': 'http://www.w3.org/2001/XMLSchema',
            'msprop': 'urn:schemas-microsoft-com:xml-msprop',
        }
        valute_data = root.find(".//xs:element", namespaces)
        on_date = valute_data.get('{urn:schemas-microsoft-com:xml-msprop}OnDate')
        return datetime.datetime.strptime(on_date, '%Y%m%d').date()

    @staticmethod
    def _body_to_request_get_curs_dynamic_xml(from_date: str, to_date: str, code_cbr: str) -> str:
        return f'''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <GetCursDynamicXML xmlns="http://web.cbr.ru/">
              <FromDate>{from_date}</FromDate>
              <ToDate>{to_date}</ToDate>
              <ValutaCode>{code_cbr}</ValutaCode>
            </GetCursDynamicXML>
          </soap:Body>
        </soap:Envelope>'''

    @staticmethod
    def _body_to_request_get_curs_on_date_xml(on_date: str) -> str:
        return f'''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <GetCursOnDate xmlns="http://web.cbr.ru/">
              <On_date>{on_date}</On_date>
            </GetCursOnDate>
          </soap:Body>
        </soap:Envelope>'''

    @staticmethod
    def _headers_request_to_cbr() -> dict:
        return {'content-type': 'text/xml'}

    @handle_http_errors
    def _request_to_cbr(self, req_body: str) -> Response:
        return self.client.post(
            config.CBR_URL,
            headers=self._headers_request_to_cbr(),
            content=req_body,
        )

    def get_curs_dynamic(self, from_date: str, to_date: str, code_cbr: str) -> t.List[dict]:
        req_body = self._body_to_request_get_curs_dynamic_xml(from_date, to_date, code_cbr)
        resp = self._request_to_cbr(req_body)
        return self._xml_to_list(resp.text, 'ValuteCursDynamic')

    def get_curs_on_date(self, on_date: str) -> tuple[list[dict], date]:
        req_body = self._body_to_request_get_curs_on_date_xml(on_date)
        resp = self._request_to_cbr(req_body)
        res = self._xml_to_list(resp.text, 'ValuteCursOnDate')
        date_response = self._get_on_date_value(resp.text)
        return res, date_response
