
API_KEY = "fabd19d1-ea48-4f06-9468-09b910a99301"

HEADER_TEXT = """
>> *Программа для обработки измерений, полученных c приборов, за определённый промежуток времени.*
"""

UPLOAD_TEXT = """
##### Для дальнейшей работы необходимо загрузить данные в формате **CSV** или **JSON** #####

Поддерживаемое расширение для формата **CSV**: .csv\n
Поддерживаемое расширение для формата **JSON**: .json, .txt
"""

DOCUMENT_TEXT = """
\tОтчёт по прибору ({}) сформирован по следующим критериям:
- Дата начала: {}
- Дата конца: {}
- Тип графика: {}
- Параметры отрисовки графика: {}
\n\tГрафик:
"""

DOCUMENT_TEXT_HEAT = """
\tГрафик теплоощущения по прибору ({}) за период с {} по {}:
"""

DOCUMENT_TEXT_LOAD = """
\tГрафик нагрузки по прибору ({}) за период с {} по {}:
"""


def frange(start, stop, step):
    while start < stop:
        yield round(float(start), 2)
        start += float(step)


HEAT = {
    "Очень жарко": list(frange(30.0, 1000.0, 0.01)),
    "Жарко": list(frange(24, 30, 0.01)),
    "Тепло": list(frange(18, 24, 0.01)),
    "Умерено тепло": list(frange(12, 18, 0.01)),
    "Прохладно": list(frange(6, 12, 0.01)),
    "Умерено": list(frange(0, 6, 0.01)),
    "Холодно": list(frange(-12, 0, 0.01)),
    "Очень холодно": list(frange(-24, -12, 0.01)),
    "Крайне холодно": list(frange(-1000, -24, 0.01)),
}

LOAD = {
    "Сильная": list(frange(30.0, 1000.0, 0.01)),
    "Умеренная": list(frange(24, 30, 0.01)) + list(frange(-12, 0, 0.01)),
    "Комфортно": list(frange(0, 24, 0.01)),
    "Сильная угроза обмораживания": list(frange(-24, -12, 0.01)),
    "Чрезвычайно высокая вероятность замерзания": list(frange(-1000, -24, 0.01))
}

YANDEX_REQUEST = 'https://api.weather.yandex.ru/v2/forecast?lat={}&lon={}&[lang=ru_RU]'

CONDITIONS = {'clear': 'Ясно', 'partly-cloudy': 'Малооблачно', 'cloudy': 'Облачно с прояснениями',
              'overcast': 'Пасмурно', 'drizzle': 'Морось', 'light-rain': 'Небольшой дождь',
              'rain': 'Дождь', 'moderate-rain': 'Умеренно сильный', 'heavy-rain': 'Сильный дождь',
              'continuous-heavy-rain': 'Длительный сильный дождь', 'showers': 'Ливень',
              'wet-snow': 'Дождь со снегом', 'light-snow': 'Небольшой снег', 'snow': 'Снег',
              'snow-showers': 'Снегопад', 'hail': 'Град', 'thunderstorm': 'Гроза',
              'thunderstorm-with-rain': 'Дождь с грозой', 'thunderstorm-with-hail': 'Гроза с градом'}


if __name__ == '__main__':
    for key in HEAT:
        print(key + ": ", HEAT[key])

    for key in LOAD:
        print(key + ": ", LOAD[key])

    print(33.01 in LOAD["Сильная"])