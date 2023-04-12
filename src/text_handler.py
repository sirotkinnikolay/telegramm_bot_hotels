from loader import bot


@bot.message_handler(content_types=['text'])
def text(message) -> None:
    """Функция обработки любого текста введенного телеграмм боту."""
    bot.send_message(message.chat.id, 'Введите одну из команд:'
                                      ' \n /lowprice - Узнать топ самых дешёвых отелей в городе'
                                      ' \n /highprice - Узнать топ самых дорогих отелей в городе'
                                      ' \n /bestdeal - Узнать топ отелей, наиболее подходящих '
                                      'по цене и расположению'
                                      ' \n /history - Узнать историю поиска отелей '
                                      '\n /help')
