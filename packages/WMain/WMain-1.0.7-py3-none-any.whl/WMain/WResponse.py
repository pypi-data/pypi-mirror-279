import lxml.etree
import requests
import lxml
from requests import Response
from typing import List
import json
class WResponse:
    
    resp: Response
    text: str
    status_code: int
    headers: dict
    url: str
    content: bytes
    
    
    def __init__(self, response: requests.Response):
        self.resp = response
        self.text = response.text
        self.status_code = response.status_code
        self.headers = response.headers
        self.url = response.url
        self.content = response.content
        
    def xpath(self, xpath: str) -> List[lxml.etree._Element]:
        html: lxml.etree._Element = lxml.etree.HTML(self.resp.text)
        return html.xpath(xpath)
        
    def json(self):
        return self.resp.json()
    