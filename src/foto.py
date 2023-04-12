from typing import List
import re
import requests
from src import config


def photos(id_hotel: str, fot_limit: str) -> List[str]:
    """Функция используя id отеля, делает запрос на rapidapi.com.
    В получееном 'json' файле по ключам находит ссылки на фотографии , удаляет с помощью регулярного
    выражения ненужную часть ссылки и записывает необходимое колличество ссылок в словарь.
    Возвращается словарь с запрашиваемым пользователем колличеством ссылок."""
    fotos_list = []
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": "{}".format(id_hotel)}

    headers = config.api_key

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=400)
    if response.status_code == 200:
        dictyonary = response.json()
        for count in range(int(fot_limit)):
            url = dictyonary['hotelImages'][count]['baseUrl']
            complite_url = re.sub(r'_\{size}', '', url)
            fotos_list.append(str(complite_url + '\n'))
    return fotos_list
