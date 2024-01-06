import typing as t
import datetime
import xml.etree.ElementTree as ET
from datetime import date
from typing import Tuple, List

from httpx import Client


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

    def _request_to_cbr(self, req_body: str) -> str:  # TODO добавить проверку кода ответа
        resp = self.client.post(
            'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx',  # TODO перенески в конфиги
            headers={
                'content-type': 'text/xml',
            },
            content=req_body,
        )
        return resp.text

    def get_curs_dynamic(self, from_date: str, to_date: str, code_cbr: str) -> t.List[dict]:
        req_body = self._body_to_request_get_curs_dynamic_xml(from_date, to_date, code_cbr)
        resp_text = self._request_to_cbr(req_body)
        return self._xml_to_list(resp_text, 'ValuteCursDynamic')

    def get_curs_on_date(self, on_date: str) -> tuple[list[dict], date]:
        req_body = self._body_to_request_get_curs_on_date_xml(on_date)
        resp_text = self._request_to_cbr(req_body)
        res = self._xml_to_list(resp_text, 'ValuteCursOnDate')
        date_response = self._get_on_date_value(resp_text)
        return res, date_response
