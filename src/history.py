import os.path
import re
from loader import bot


@bot.message_handler(commands=['history'])
def history(message) -> None:
    """Функция обработки команды телеграмм боту 'history'. Открывает файл 'history_list.txt',
    с помощью регулярного выражения проверят, является ли строка ссылкой, если строка содержит
    ссылку, то отправляет ее пользователю  как изображение, если нет то как текстовое сообщение.
    Если файла 'history_list.txt' не существует или он пуст то обрабатывается ошибка
    'FileNotFoundError' ,сообщает об этом пользователю   """
    try:
        history_file = os.path.abspath('history_list.txt')
        with open(history_file, 'r', encoding='utf-8') as file:
            bot.send_message(message.chat.id, 'история запросов:')
            for element in file:
                one = re.search(r"(?P<url>https?://[^\s]+)", element)
                if one:
                    bot.send_photo(message.chat.id, element)
                else:
                    bot.send_message(message.chat.id, element)

    except FileNotFoundError:
        bot.send_message(message.chat.id, 'история запросов пуста.\nВведите одну из команд:'
                                      ' \n /lowprice \n /highprice \n '
                                      '/bestdeal \n /history')
