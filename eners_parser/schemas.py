from dataclasses import dataclass
from enum import Enum
from datetime import date, time


@dataclass
class Event:
    event_date: date
    start_time: time
    end_time: time


class LessonType(Enum):
    UNKNOWN = "UNKNOWN"
    LECTURE = "Лекция"
    PRACTICE = "Практика"
    LAB = "Лабораторная"
    EXAM = "Экзамен"


@dataclass
class Lesson(Event):
    name: str
    cabinet: str
    teacher: str
    type: LessonType