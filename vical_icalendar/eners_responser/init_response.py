import requests
import datetime
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from eners_parser.re_patterns import *
from operator import xor
from calendar import monthrange


class InitResponse():
    __headers = {
        "User-Agent": UserAgent(use_external_data=True).random
    }
    __url = 'https://eners.kgeu.ru/apish2.php'
    __group_name: str
    __week_id = 1
    __response: str
    __soup: BeautifulSoup
    __start_date: datetime.date
    __start_week: int = 0
    __end_week: int = 0

    def __init__(
            self,
            group_name: str,
            is_month: bool = False,
            is_week: bool = False,
            is_next: bool = False
    ):
        self.__response = requests.get(self.__url + f'?group={group_name}&week={self.__week_id}&type=one',
                                       headers=self.__headers).text
        self.__soup = BeautifulSoup(self.__response, 'lxml')
        days = self.__soup.find_all(attrs={"class": "card"})
        for day in days:
            if (date_init := re.search(RE_DATE, (day.find_next(attrs={"class": "card-header"}).text))) is None:
                continue
            else:
                self.__start_date = datetime.date(
                    year=int(date_init.group(3)),
                    month=int(date_init.group(2)),
                    day=int(date_init.group(1))
                )
                break

        if xor(is_month, is_week) and (self.__start_date is not None):
            current_date = self.__start_date
            user_date = datetime.date.today()
            self.__start_week = 1
            delta = datetime.timedelta(weeks=1)
            if is_month:
                while (current_date + self.__start_week * delta).month != (user_date.month + is_next):
                    self.__start_week += 1
                self.__end__week = self.__start_week
                while (current_date + self.__end__week * delta).month == (user_date.month + is_next):
                    self.__end__week += 1
            if is_week:
                while (current_date + self.__start_week * delta) <= (user_date + is_next * delta):
                    self.__start_week += 1
                self.__end__week = self.__start_week
        else:
            pass

    def get_weeks_range(self):
        return range(self.__start_week, self.__end__week + 1)
