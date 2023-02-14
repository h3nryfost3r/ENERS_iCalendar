import re

from bs4 import BeautifulSoup
from datetime import date, time
from typing import List

from vical_icalendar.parser_handler.re_patterns import *
from vical_icalendar.response_handler.handler import ResponseHandler
from vical_icalendar.parser_handler.schemas import Lesson, LessonType


class InitParser:
    __soup: BeautifulSoup
    __response_handler: ResponseHandler

    def __init__(self, group_name, weeks_range: range):
        self.__response_handler = ResponseHandler(group_name=group_name, weeks_range=weeks_range)
        self.__soup = BeautifulSoup(''.join(
            self.__response_handler.get_responses()), 'lxml')

    def get_soup(self):
        return self.__soup


class ParserHandler(InitParser):
    __lessons: List[Lesson] = list()

    def __init__(
            self,
            group_name,
            weeks_range: range,
            is_month: bool = False,
            is_next: bool = False
    ):
        super().__init__(group_name, weeks_range)
        days = self.get_soup().find_all(attrs={"class": "card"})
        for day in days:
            self.__get_day_events(day, is_month, is_next)

    def __get_day_events(
            self,
            day: BeautifulSoup,
            is_month: bool,
            is_next: bool
    ):
        if re.search(
                RE_DATE,
                (lesson_header := day.find_next(attrs={"class": "card-header"}).text)
        ) is None:
            return

        lessons_date_re = re.search(RE_DATE, lesson_header)

        lessons_date = date(
            year=int(lessons_date_re.group(3)),
            month=int(lessons_date_re.group(2)),
            day=int(lessons_date_re.group(1))
        )

        if is_month and lessons_date.month != (date.today().month + is_next):
            return

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

            lesson_type: LessonType = LessonType.LECTURE if str(re.search(RE_LESSON, event).group(1)) == 'л.' else \
                LessonType.PRACTICE if str(re.search(RE_LESSON, event).group(1)) == 'пр.' else \
                    LessonType.LAB if str(re.search(RE_LESSON, event).group(1)) == 'лаб.' else \
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
