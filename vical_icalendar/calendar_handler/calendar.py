from typing import List

import icalendar as ical
from vical_icalendar.parser_handler import schemas
from datetime import datetime
import pytz
from uuid import uuid4


class ICalendarHandler:
    cal: ical.Calendar
    _tz_str: str = 'Europe/Moscow'
    __tz_info = pytz.timezone(_tz_str)

    def __init__(self, data: List[schemas.Lesson]):
        self.tz = pytz.timezone(self._tz_str)
        self.cal = ical.Calendar({
            'prodid': '-//VICAL vALPHA//',
            'version': '2.0',
            'tzid': self.__tz_info,
            'method': 'PUBLISH'
        })
        for event in data:
            self.__add_event(event)

    def __add_event(self, lesson: schemas.Lesson):
        self.cal.add_component(
            self.__generate_ical_Event(lesson))
        return True
    
    def __generate_ical_Event(self, lesson: schemas.Lesson):
        event = ical.Event({
            'uid': uuid4(),
            'summary': f'{lesson.type.value}\n'
                       f'{lesson.name}\n'
                       f'{lesson.cabinet}\n'
                       f'{lesson.teacher}'
        })
        event.add('dtstart', datetime.combine(
            lesson.event_date, lesson.start_time, tzinfo=self.__tz_info))
        event.add('dtend', datetime.combine(
            lesson.event_date, lesson.end_time, tzinfo=self.__tz_info))
        event.add('dtstamp', datetime.now(tz=self.__tz_info))
        return event
    

    def write_ical(self, path='./file.ics'):
        with open(path, 'wb') as f:
            f.write(self.cal.to_ical())
        return True

    def __get_ical_from_file(self, path: str):
        new_ical: ical.Calendar
        with open(path, 'rb') as file:
            new_ical = ical.Calendar.from_ical(file.read())
        return new_ical

    @staticmethod
    def update_ical(
            cal_a: ical.Calendar,
            cal_b: ical.Calendar
    ):
        pass


    @staticmethod
    def get_diff(
            cal_a: ical.Calendar,
            cal_b: ical.Calendar
    ):
        pass

    def __repr__(self):
        return self.cal.__str__()
