from typing import Optional
import itertools
import requests
from src import config, foto


def city_change(city: str) -> Optional[str]:
    """Функция принимает название города на английском языке, и делает запрос на rapidapi.com,
     находит  destinationId
    города, если такого города не существует передается None"""
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": None, "currency": None}

    headers = config.api_key

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=400)
    dictyonary = response.json()
    if response.status_code == 200:
        destination_id = dictyonary['suggestions'][0]['entities'][0]['destinationId']
        return str(destination_id)
    return None


def best_high_deal(city: str, hotel_limit: int, d_start: str, d_end: str, filt: str,
                   min_price: Optional[int], max_price: Optional[int], limit: str,
                   min_dist: float, max_dist: float) -> None:
    """Функция используя введенные пользователем данные из экземпляра класса 'all_users',
    делает запрос на rapidapi.com. Проверяет статус запроса, если он совершен без ошибок,
    то находит в 'json' файле нужные данные по ключам словаря и записывает их в файл 'bufer.txt',
    перед эти очищая его. Если по искомым ключам данные отсутствуют то обрабатывается ошибка
    'KeyError', в файл записывается что данные отсутствуют по данному запросу.  Делает
    сортировку отелей по расстоянию от центра при введении комады 'bestdeal' и выводит только те,
    которрые удовлетворяют условию поиска. С помощью функции 'photos', выполняется запрос и
    записывается в файл необходимое пользователю колличество ссылок на фотографии отеля. Если запрос
    не может быть совершен, выводится соответствующее сообщение пользователю."""
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        headers = config.api_key
        querystring = {"destinationId": city, "pageNumber": "1", "pageSize": "25",
                       "checkIn": d_start, "checkOut": d_end, "adults1": "1",
                       "priceMin": min_price, "priceMax": max_price,
                       "sortOrder": filt, "landmarkIds": "City Center",
                       "locale": None, "currency": None}

        response = requests.request("GET", url, headers=headers, params=querystring, timeout=400)
        if response.status_code == 200:
            dictyonary = response.json()
            open('bufer.txt', 'w').close()
            with open('bufer.txt', 'a', encoding='utf-8') as file:
                base = dictyonary['data']['body']['searchResults']['results']
                natural_num = itertools.count(1)
                cifer = 0
                for i in natural_num:
                    if float(min_dist) < float(base[i]['landmarks'][0]
                                               ['distance'][:3]) < float(max_dist):
                        try:
                            file.write('Сайт отеля: ' + 'hotels.com/ho' +
                                       str(base[i]['id']) + '\n')
                        except KeyError:
                            file.write('Сайт отеля: Информация отсутствует' + '\n')
                        try:
                            file.write('Название отеля: ' + str(base[i]['name']) + '\n')
                        except KeyError:
                            file.write('Название отеля: Информация отсутствует' + '\n')
                        try:
                            file.write('Адрес: ' + str(base[i]['address']
                                                       ['streetAddress']) + '\n')
                        except KeyError:
                            file.write('Адрес: Информация отсутствует' + '\n')
                        try:
                            file.write('Расстояние от центра: ' + str(base[i]['landmarks']
                                                                      [0]['distance']) + '\n')
                        except KeyError:
                            file.write('Расстояние от центра: Информация отсутствует' + '\n')
                        try:
                            file.write('Цена за день: ' + str(base[i]['ratePlan']['price']
                                                              ['current']) + '\n')
                        except KeyError:
                            file.write('Цена за день: Информация отсутствует' + '\n')
                        try:
                            file.write(
                                'Общая стоимость: ' + str(base[i]['ratePlan']['price']
                                                          ['fullyBundledPricePerStay'][6:13])
                                + '\n')
                        except KeyError:
                            file.write('Общая стоимость: Информация отсутствует' + '\n')

                        for count in foto.photos(id_hotel=base[i]['id'], fot_limit=limit):
                            file.write(str(count))
                        cifer += 1
                        if cifer == int(hotel_limit):
                            break
                    else:
                        continue
        else:
            with open('bufer.txt', 'a', encoding='utf-8') as file:
                file.write('Ваш запрос не может быть обработан:\n код ошибки {} \n'
                           .format(response.status_code))
    except IndexError:
        with open('bufer.txt', 'a', encoding='utf-8') as file:
            file.write('По вашему запросу ничего не найденно. ')
