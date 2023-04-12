import os
from datetime import datetime
from datetime import date
import re
from typing import Any
from googletrans import Translator
from loader import bot



def translator(text: str) -> str:
    """Полученное текстовое значение переводится с помощью функции 'Translator', с русского
    языка н английский. Возвращается тестовое значение на английском языке"""
    us_translator = Translator()
    translation = us_translator.translate(text, dest='en')
    return translation.text


def date_check(date_str: str) -> bool:
    """Полученное текстовое значение даты приводится в установленный формат функцией
    'datetime.strptime', далее проверяется что бы полученная дата не была раньше даты
    запуска данной функции. Если дата позднее даты запуска функции то возвращвется
    '1', в противном случае '0' """
    user_date = datetime.strptime(date_str, '%Y-%m-%d')
    today = datetime.now()
    if user_date > today:
        return True
    return False


def is_float(string: str) -> Any:
    """Полученное текстовое значение проверяется на совпадение с шаблоном, с помощь
    регулярного выражения. Если сопадает то возвращется равенство, иначе 'False' """
    check = re.match(r'\d*\.?\d+', string)
    if check:
        return check.group() == string
    return False


def history_write(name: str) -> None:
    """Функция записывает в файл 'history_list.txt', хранящий историю запросов ,
    название команды запроса, дату запроса и результат запроса."""
    with open('history_list.txt', 'a', encoding='utf-8') as file:
        file.write('=====Команда для поиска: {}====='.format(name) + '\n')
        file.write(str(date.today()) + '\n')
        bufer_file = os.path.abspath('bufer.txt')
        with open(bufer_file, 'r', encoding='utf-8') as files:
            for hist in files:
                file.write(hist)


def send_mes(message: Any) -> None:
    """Функция считывает текстовые данные из файла 'bufer.txt', если строка является
    текстом то посылает пользователю в телеграмм боте текстовое сообщение. Если строка
    является ссылкой то посылает сообщение в виде фото."""
    bufer_file = os.path.abspath('bufer.txt')
    with open(bufer_file, 'r', encoding='utf-8') as file:
        for line in file:
            one = re.search(r"(?P<url>https?://[^\s]+)", line)
            if one:
                bot.send_photo(message.chat.id, line)
            else:
                bot.send_message(message.chat.id, line)
