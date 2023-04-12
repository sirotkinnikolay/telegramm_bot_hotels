"""Класс"""


class User:
    """В экземпляре данного класса хранятся данные, которые вводит пользователь,
    при поиске отелей"""

    def __init__(self) -> None:
        self.date_start = None
        self.date_end = None
        self.city = None
        self.hotels_limit = None
        self.foto_limit = None
        self.min_price = None
        self.max_price = None
        self.min_distance = None
        self.max_distance = None
        self.com = None
