import typing as t
import xml.etree.ElementTree as ET

from httpx import Client


class CBRAdapter:
    def __init__(self):
        self.client = Client()

    @staticmethod
    def xml_to_list(xml_str: str) -> t.List[dict]:
        root = ET.fromstring(xml_str)
        valute_curs_dynamic_elements = root.findall(".//ValuteCursDynamic")
        response_list = []
        for valute_curs_dynamic in valute_curs_dynamic_elements:
            response_list.append({
                'CursDate': valute_curs_dynamic.findtext("CursDate"),
                'Vcode': valute_curs_dynamic.findtext("Vcode"),
                'Vnom': valute_curs_dynamic.findtext("Vnom"),
                'Vcurs': valute_curs_dynamic.findtext("Vcurs"),
                'VunitRate': valute_curs_dynamic.findtext("VunitRate")
            })
        return response_list

    @staticmethod
    def body_to_request_get_curs_dynamic_xml(from_date: str, to_date: str, code_cbr: str) -> str:
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

    def get_curs_dynamic(self, from_date: str, to_date: str, code_cbr: str):
        req_body = self.body_to_request_get_curs_dynamic_xml(from_date, to_date, code_cbr)
        resp = self.client.post(
            'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx',
            headers={
                'content-type': 'text/xml',
            },
            content=req_body,
        )
        resp_list = self.xml_to_list(resp.text)
        return resp_list
