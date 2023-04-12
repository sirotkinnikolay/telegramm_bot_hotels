import logging
from loader import bot
from src import handlers, history, text_handler



logging.basicConfig(
    level=logging.ERROR,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

while True:
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True, interval=0)
    except Exception as problem:
        logging.error(problem)
