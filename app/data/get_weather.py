import json

import pandas as pd
import requests

from app.config import API_KEY, YANDEX_REQUEST, CONDITIONS


def yandex_weather(latitude, longitude):
    url_yandex = YANDEX_REQUEST.format(latitude, longitude)
    yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': API_KEY}, verify=False)

    yandex_json = json.loads(yandex_req.text)
    yandex_json['fact']['condition'] = CONDITIONS[yandex_json['fact']['condition']]

    pogoda = {}
    pogoda["city"] = yandex_json["info"]["tzinfo"]["name"].split("/")[1]
    params = ['condition', 'wind_speed', 'pressure_mm', 'humidity']

    pogoda['fact'] = dict()
    pogoda['fact']['temp'] = yandex_json['fact']['temp']
    for param in params:
        pogoda['fact'][param] = yandex_json['fact'][param]

    pogoda['link'] = yandex_json['info']['url']
    return pogoda


def _main():
    pass


if __name__ == '__main__':
    _main()
