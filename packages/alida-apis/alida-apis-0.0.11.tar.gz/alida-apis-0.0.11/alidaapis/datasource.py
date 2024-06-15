from .utils import read_var
from .auth import _get_token
import requests, json

def get_all():
    
    url = read_var("url_base") + read_var("url_datasources")
    
    payload = {}
    headers = {
        'authorization': 'Bearer ' + _get_token(),
    }

    return requests.request("GET", url, headers=headers, data=payload)

def get_by_id(id):
    datasources = json.loads(get_all().text)
    for datasource in datasources:
        if int(datasource['id']) == int(id):
            return datasource


def get_by_name(name):
    datasources = json.loads(get_all().text)
    for datasource in datasources:
        if datasource['name'] == name:
            return datasource
