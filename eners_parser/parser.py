from bs4 import BeautifulSoup
from datetime import date, time
from typing import List

from .schemas import Lesson, LessonType
from .re_patterns import *

from eners_responser.handler import ResponseHandler

class InitParser:

    __soup: BeautifulSoup
    __response_handler: ResponseHandler

    def __init__(self, group_name):
        self.__response_handler = ResponseHandler(group_name=group_name)
        self.__soup = BeautifulSoup(''.join(
            self.__response_handler.get_responses()), 'lxml')


class ParserHandler(InitParser):
    __lessons: List[Lesson] = list()

    def __init__(self, data):
        # getting __soup from super class
        super().__init__(data)

        # handle __soup to get events
        days = self.__soup.find_all(attrs={"class": "card"})

        for day in days:
            self.__get_day_events(day)

    def __get_day_events(self, day: BeautifulSoup):
        if day.find_next(attrs={"class": "list-group_name list-group_name-striped"}).text.strip() == "Пары отсутствуют":
            return
        lessons_date_re = re.search(
            RE_DATE, day.find_next(attrs={"class": "card-header"}).text
        )
        lessons_date = date(
            year=int(lessons_date_re.group(3)),
            month=int(lessons_date_re.group(2)),
            day=int(lessons_date_re.group(1))
        )

        for event in map(
                lambda x: x.text.strip(), day.find_all('li')
        ):
            lesson_time_re = re.search(RE_TIME, event)

            lesson_time_start = time(
                hour=int(lesson_time_re.group(2)),
                minute=int(lesson_time_re.group(3))
            )

            lesson_time_end = time(
                hour=int(lesson_time_re.group(5)),
                minute=int(lesson_time_re.group(6))
            )

            lesson_type: LessonType = LessonType.LECTURE if str(re.search(RE_LESSON, event).group(1)) == 'л' else \
                LessonType.PRACTICE if str(re.search(RE_LESSON, event).group(1)) == 'пр' else \
                    LessonType.LAB if str(re.search(RE_LESSON, event).group(1)) == 'лаб' else \
                        LessonType.EXAM if str(re.search(RE_LESSON, event).group(1)) == 'экзамен' else \
                            LessonType.UNKNOWN

            lesson_name = str(re.search(RE_LESSON, event).group(2))
            lesson_cabinet = str(re.search(RE_CABINET, event).group(1))
            lesson_teacher = str(re.search(RE_TEACHER, event).group(1))

            self.__lessons.append(Lesson(
                event_date=lessons_date,
                start_time=lesson_time_start,
                end_time=lesson_time_end,
                name=lesson_name,
                cabinet=lesson_cabinet,
                teacher=lesson_teacher,
                type=lesson_type
            ))

    def get_lessons(self):
        return self.__lessons.copy()
