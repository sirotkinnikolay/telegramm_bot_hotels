import datetime
from datetime import datetime
from src import utils, models, api
from loader import bot


all_users: dict = {}

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def command(message) -> None:
    """При введении команд 'lowprice', 'highprice', 'bestdeal', запускается функция 'command',
    создается экземпляр класса 'User', удаляются все элементы списка 'com', и в список
    записывается значение равное введенной команде. далее запускается функция 'date_start'."""
    all_users[message.chat.id] = models.User()
    date_start(message)
    all_users[message.chat.id].com = message.text


def date_start(message) -> None:
    """Запускается функция 'date_start', у пользователя запрашивается дата заезда в гостинницу.
    Делее полученноезначения передается в функцию  'date_end'."""
    bot.send_message(message.chat.id, 'Введите дату заезда (гггг-мм-дд):')
    bot.register_next_step_handler(message, date_end)


def date_end(message) -> None:
    """запускается функция 'date_end',запускается функция 'date_check', которая проверяет
    что бы введенная дата не была раньше дня запуска функции и возвращет '1' если дата введена
    корректно или '0' если нет, если дата введена неверно или тип введенных данных не
    соответствует , то она запрашивается снова, если верно то она присваивается значению
    'date_start' экземпляра класса 'all_users'. Запрашивается дата выезда из гостинницы.
    Далее полученное значение передается в функцию 'begin_low'."""
    try:
        start = message.text
        if not utils.date_check(start):
            bot.send_message(message.chat.id, 'Введенная дата не может быть '
                                              'раньше сегодняшнего дня.')
            date_start(message)
        else:
            all_users[message.chat.id].date_start = start
            bot.send_message(message.chat.id, 'Введите дату выезда (гггг-мм-дд):')
            bot.register_next_step_handler(message, begin_low)
    except ValueError:
        date_start(message)


def date_end_repeat(message) -> None:
    """Функция повторного запроса даты выезда из гостинницы. Далее введенное значение
    передается в функцию 'begin_low'."""
    bot.send_message(message.chat.id, 'Введите дату выезда (гггг-мм-дд):')
    bot.register_next_step_handler(message, begin_low)


def begin_low(message) -> None:
    """Запускается функция 'begin_low'. запускается функция 'date_check', которая проверяет
    что бы введенная дата небыла раньше дня запуска функции и возвращет '1' если дата введена
    корректно или '0' если нет, если дата введена неверно или тип введенных данных не
    соответствует , то она запускает функцию 'date_end_repeat' и запрашивает снова,
    если дата выезда введена раньше даты заезда, то она запускается функция 'date_end_repeat'
    и запрашивает снова. Если дата выезда введна верно то она присваивается значению
    'date_end' экземпляра класса 'all_users'. У пользователя запрашивается город для поиска
    отелей, значение передается в функцию 'get_city'. """
    try:
        end = message.text
        if not utils.date_check(end):
            bot.send_message(message.chat.id, 'Дата выезда не может быть '
                                              'раньше сегодняшнего дня')
            date_end_repeat(message)
        elif datetime.strptime(all_users[message.chat.id].date_start,
                               '%Y-%m-%d') > datetime.strptime(end, '%Y-%m-%d'):
            bot.send_message(message.chat.id, 'Дата выезда не может быть раньше даты заезда')
            date_end_repeat(message)
        else:
            all_users[message.chat.id].date_end = end
            bot.send_message(message.chat.id, 'В каком городе ищем отель?')
            bot.register_next_step_handler(message, get_city)
    except ValueError:
        date_end_repeat(message)


def get_city(message) -> None:
    """Название города с помощью функции 'translator' переводится на английски и в нижний
    регистр и присваивается переменной 'city' экземпляра класса 'all_users'. У пользователя
    запрашивается коллличество отелей для поиска. Значение передается в функцию
    'get_hotels_limit'."""
    city = message.text
    all_users[message.chat.id].city = utils.translator(city).lower()
    print(all_users[message.chat.id].city)
    bot.send_message(message.chat.id, 'Какое колличество отелей?')
    bot.register_next_step_handler(message, get_hotels_limit)


def repeat_hotels_limit(message) -> None:
    """Функция повторного запроса колличества отелей для поиска. Полученное значение
     передается в функцию
    'get_hotels_limit'."""
    bot.send_message(message.chat.id, 'Какое колличество отелей?')
    bot.register_next_step_handler(message, get_hotels_limit)


def get_hotels_limit(message) -> None:
    """Запускается функция 'get_hotels_limit'. С помощью функции 'isdigit', проверяется
    введенное значение.Если оно является цифровым оно меньше установленного лимита '10',
    и больше '0', то оно присваивается значению 'hotel_limit'экземпляра класса 'all_users'.
    У пользователя спрашивается хочет ли он загрузить фото для каждого отеля.
    Значение передается в функцию 'get_foto_answer'.Если значение введено не верно,
    то запускается функция повторного запроса 'repeat_hotels_limit'. """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            all_users[message.chat.id].hotels_limit = int(message.text)
            bot.send_message(message.chat.id, 'Загрузить фото для каждого отеля? ДА/НЕТ')
            bot.register_next_step_handler(message, get_foto_answer)
        else:
            repeat_hotels_limit(message)
    else:
        repeat_hotels_limit(message)


def repeat_foto_limit(message) -> None:
    """Функция повторного запроса колличества выводимых фотографий для каждого отеля.
    Далее значение передается в функцию 'get_foto_limit'."""
    bot.send_message(message.chat.id, 'Какое колличество фотографий необходимо загрузить?')
    bot.register_next_step_handler(message, get_foto_limit)


def repeat_answer(message) -> None:
    """Функция повторного запроса вывода фотографий для каждого отеля. Далее значение
    передается в функцию 'get_foto_answer'."""
    bot.send_message(message.chat.id, 'Некорректный ответ, вариант ответа:\nДА/НЕТ')
    bot.register_next_step_handler(message, get_foto_answer)


def get_foto_answer(message) -> None:
    """Запускается функция 'get_foto_answer'. Если полученное значение равно 'да', то у
    пользователя запрашивается колличество фотографий, которое необходимо загрузить для
    каждого отеля. Значение передается в функцию 'get_foto_limit'. Если полученное значение
    равно 'нет',то значению 'foto_limit' экземпляра класса 'all_users'
    присваивается значение '0'. Проверяется чему равен элемент с нулевым индексом в списке
    'com' и вызывается соответтствующая команда. 'prints_low', 'prints_high', 'get_city_best' .
    Если полученное значение не равно 'да'или 'нет', то вызывается функция 'repeat_answer'
    и ответ запрашивается повторно"""
    foto_answer = message.text
    if foto_answer.lower() == 'да':
        bot.send_message(message.chat.id, 'Какое колличество фотографий необходимо загрузить?')
        bot.register_next_step_handler(message, get_foto_limit)
    elif foto_answer.lower() == 'нет':
        all_users[message.chat.id].foto_limit = 0
        if all_users[message.chat.id].com == '/lowprice':
            prints_low(message)
        elif all_users[message.chat.id].com == '/highprice':
            prints_high(message)
        elif all_users[message.chat.id].com == '/bestdeal':
            get_city_best(message)
    else:
        repeat_answer(message)


def get_foto_limit(message) -> None:
    """Если ранее был введен ответ 'да', то запускается функция 'get_foto_limit'.
    С помощью функции 'isdigit',проверяется введенное значение.Если оно является цифровым
    оно меньше установленного лимита '10' и больше '0', то оно присваивается значению
    'foto_limit'экземпляра класса 'all_users'.Проверяется чему равен элемент с нулевым
    индексом в списке 'com' и вызывается соответтствующая команда. 'prints_low', 'prints_high',
    'get_city_best'. Если полученное значение не является цифровым или больше, установленно
    лимита, то вызывается функция 'repeat_foto_limit', которая повторно запрашивает колличество
    выводимых фотографий для каждого отеля."""
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            all_users[message.chat.id].foto_limit = message.text
            if all_users[message.chat.id].com == '/lowprice':
                prints_low(message)
            elif all_users[message.chat.id].com == '/highprice':
                prints_high(message)
            elif all_users[message.chat.id].com == '/bestdeal':
                get_city_best(message)
        else:
            bot.send_message(message.chat.id, 'Превышен лимит по запросу фотографий.')
            repeat_foto_limit(message)
    else:
        repeat_foto_limit(message)


def prints_low(message) -> None:
    """Функция запроса с сайта rapidapi.com, по значениям экземпляра класса 'all_users',
    при введении пользователем команды запроса 'lowprice'. Запускается функция  'best_high_deal'
    в нее из экземпляра класса передаются значения. Далее запускается функция 'send_mes', для
    вывода в собщениях телеграмм бота информации для пользователя.
    Запускается функция 'history_write', которая записыввет в текстовый файл информацию
    данного запроса с названиемкоманды, введенной пользователем и датой введенной команды. """
    api.best_high_deal(city=api.city_change(all_users[message.chat.id].city),
                       hotel_limit=all_users[message.chat.id].hotels_limit,
                       d_start=all_users[message.chat.id].date_start,
                       d_end=all_users[message.chat.id].date_end,
                       filt='PRICE_LOW_FIRST', min_price=None,
                       max_price=None, limit=all_users[message.chat.id].foto_limit,
                       max_dist=100.0, min_dist=0.0)
    utils.send_mes(message)
    utils.history_write('lowprice')


def prints_high(message) -> None:
    """Функция запроса с сайта rapidapi.com, по значениям экземпляра класса 'all_users',
    при введении пользователем команды запроса 'highprice'. Запускается функция
    'best_high_deal' в нее из экземпляра класса передаются значения. Далее запускается функция
    'send_mes', для вывода в собщениях телеграмм бота информации для пользователя.
    Запускается функция 'history_write', которая записыввет в текстовый файл информацию
    данного запроса с названиемкоманды, введенной пользователем и датой введенной команды. """
    api.best_high_deal(city=api.city_change(all_users[message.chat.id].city),
                       hotel_limit=all_users[message.chat.id].hotels_limit,
                       d_start=all_users[message.chat.id].date_start,
                       d_end=all_users[message.chat.id].date_end,
                       filt='PRICE_HIGHEST_FIRST', min_price=None,
                       max_price=None, limit=all_users[message.chat.id].foto_limit,
                       max_dist=100.0, min_dist=0.0)

    utils.send_mes(message)
    utils.history_write('highprice')


def get_city_best(message) -> None:
    """Если пользователем была введена команда 'bestdeal', то после функции 'get_foto_limit',
    запускается функция 'get_city_best', она запрашивает минимальную цену для поиска отеля.
    Полученное значение передается в функцию 'min_price'."""
    bot.send_message(message.chat.id, 'Минимальная цена отеля?')
    bot.register_next_step_handler(message, min_price)


def min_price_r(message) -> None:
    """Функция повторного запроса минимальной уены отеля, полученное значение передает в
    функцию 'min_price'."""
    bot.send_message(message.chat.id, 'Минимальная цена отеля?')
    bot.register_next_step_handler(message, min_price)


def min_price(message) -> None:
    """Запускается функция 'min_price'. Если полученное значение является цифровым и
    больше '0',то оно присваивается значению 'min_price'экземпляра класса 'all_users',
    у пользователя запрашивается максимальная цена отеля. Значение
    передается в функцию 'max_price'. Если полученное значение не удовлетворяет
    требованиям , то запускатся функция повторного запроса минимальной цены отеля 'min_price_r' """
    if message.text.isdigit():
        if int(message.text) > 0:
            all_users[message.chat.id].min_price = int(message.text)
            bot.send_message(message.chat.id, 'Максимальная цена отеля? ')
            bot.register_next_step_handler(message, max_price)
        else:
            min_price_r(message)
    else:
        min_price_r(message)


def max_price_r(message) -> None:
    """Функция повторного запроса максимальной уены отеля, полученное значение
    передает в функцию 'max_price'."""
    bot.send_message(message.chat.id, 'Максимальная цена отеля?')
    bot.register_next_step_handler(message, max_price)


def max_price(message) -> None:
    """Запускается функция 'max_price'. Если полученное значение является цифровым и
    больше '0',то оно присваивается значению 'max_price'экземпляра класса 'all_users',
    у пользователя запрашивается минимально расстояние расположения отеля от центра города.
    Значение передается в функцию 'distance'. Если полученное значение не удовлетворяет
    требованиям , то запускатся функция повторного запроса максимальной цены отеля 'max_price_r' """
    if message.text.isdigit():
        if int(message.text) > all_users[message.chat.id].min_price:
            all_users[message.chat.id].max_price = int(message.text)
            bot.send_message(message.chat.id, 'Минимальное расстояние от центра? ')
            bot.register_next_step_handler(message, distance)
        else:
            bot.send_message(message.chat.id, 'Максимальная цена не может '
                                              'быть меньше минимальной.')
    else:
        max_price_r(message)


def min_distance_repeat(message) -> None:
    """Функция повторного запроса минимально расстояния расположения отеля от
    центра города , полученное значение передает в функцию 'distance'."""
    bot.send_message(message.chat.id, 'Минимальное расстояние от центра? ')
    bot.register_next_step_handler(message, distance)


def max_distance_repeat(message) -> None:
    """Функция повторного запроса максимального расстояния расположения отеля от
    центра города , полученное значение передает в функцию 'max_distance'."""
    bot.send_message(message.chat.id, 'Максимальнео расстояние от центра? ')
    bot.register_next_step_handler(message, max_distance)


def distance(message) -> None:
    """Запускается функция 'distance'. Запускается функция 'is_float', которая проверяет ,
    является ли введенное значениечисло дробным числом. Если да, то оно присваивается значению
    'min_distance'экземпляра класса 'all_users'. У пользователя запрашивается максимальное
    расположение отеля от центра города. Полученное значение передается в
    функцию  'max_distance'. Если полученное значение не удовлетворяет условиям или введено
    не корректно то запускается функция повторного запроса минамальной дистанции
    'min_distance_repeat'"""
    if utils.is_float(message.text):
        all_users[message.chat.id].min_distance = float(message.text)
        bot.send_message(message.chat.id, 'Максимальное расстояние от центра?')
        bot.register_next_step_handler(message, max_distance)
    else:
        min_distance_repeat(message)


def max_distance(message) -> None:
    """Запускается функция 'max_distance'. Запускается функция 'is_float', которая проверяет ,
    является ли введенное значениечисло дробным числом. Если да, то оно присваивается значению
    'max_distance'экземпляра класса 'all_users'. Запускается функция 'prints_best'. Если
    полученное значение не удовлетворяет условиям или введено не корректно то запускается
    функция повторного запроса максимальной дистанции 'max_distance_repeat'"""
    if utils.is_float(message.text):
        if float(message.text) > all_users[message.chat.id].min_distance:
            all_users[message.chat.id].max_distance = float(message.text)
            bot.register_next_step_handler(message, prints_best(message))
        else:
            bot.send_message(message.chat.id, 'Максимальное расстояние не может'
                                              ' быть меньше минимального.')
            max_distance_repeat(message)
    else:
        max_distance_repeat(message)


def prints_best(message) -> None:
    """Функция запроса с сайта rapidapi.com, по значениям экземпляра класса 'all_users',
    при введении пользователем команды запроса 'bestdeal'. Запускается функция  'best_high_deal'
    в нее из экземпляра класса передаются значения. Далее запускается функция 'send_mes',
    для вывода в собщениях телеграмм бота информации для пользователя. Запускается функция
    'history_write', которая записыввет в текстовый файл информацию данного запроса с названием
    команды, введенной пользователем и датой введенной команды. Если по запросам пользователя
    ничего не найденно, то генерируется ошибка 'Exception', она обрабатывается и пользователю
    выводится сообщение о том что по его запросу ничего не найдено."""
    api.best_high_deal(city=api.city_change(all_users[message.chat.id].city),
                           hotel_limit=all_users[message.chat.id].hotels_limit,
                           d_start=all_users[message.chat.id].date_start,
                           d_end=all_users[message.chat.id].date_end,
                           filt="DISTANCE_FROM_LANDMARK",
                           min_price=all_users[message.chat.id].min_price,
                           max_price=all_users[message.chat.id].max_price,
                           limit=all_users[message.chat.id].foto_limit,
                           max_dist=all_users[message.chat.id].max_distance,
                           min_dist=all_users[message.chat.id].min_distance)

    utils.send_mes(message)
    utils.history_write('bestdeal')
