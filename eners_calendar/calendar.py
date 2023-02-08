from typing import List
import icalendar as ical
from eners_parser import schemas
from datetime import datetime
import pytz
from uuid import uuid4


class EnersCalendarHandler:
    cal: ical.Calendar
    cal_tz_str: str = 'Europe/Moscow'
    __cal_tz_info = pytz.timezone(cal_tz_str)

    def __init__(self, data):
        self.tz = pytz.timezone(self.cal_tz_str)
        self.cal = ical.Calendar({
            'prodid': '-//ENERS calendar vALPHA//',
            'version': '2.0',
            'tzid': self.__cal_tz_info,
            'method': 'PUBLISH'
        })

    def __generate_ical_Event(self, lesson: schemas.Lesson):
        event = ical.Event({
            'uid': uuid4(),
            'summary': f'{lesson.type.value}\n'
                       f'{lesson.name}\n'
                       f'{lesson.cabinet}\n'
                       f'{lesson.teacher}'
        })
        event.add('dtstart', datetime.combine(
            lesson.event_date, lesson.start_time, tzinfo=self.__cal_tz_info))
        event.add('dtend', datetime.combine(
            lesson.event_date, lesson.end_time, tzinfo=self.__cal_tz_info))
        event.add('dtstamp', datetime.now(tz=self.__cal_tz_info))
        return event

    def add_event(self, lesson: schemas.Lesson):
        self.cal.add_component(
            self.__generate_ical_Event(lesson))
        return True


    def write_ical(self, path='./file.ics'):
        with open(path, 'wb') as f:
            f.write(self.cal.to_ical())
        return True

    def __repr__(self):
        return self.cal.__str__()
