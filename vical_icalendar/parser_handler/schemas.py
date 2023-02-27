from dataclasses import dataclass
from enum import Enum
from datetime import date, time

class LessonType(Enum):
    UNKNOWN = "UNKNOWN"
    LECTURE = "Лекция"
    PRACTICE = "Практика"
    LAB = "Лабораторная"
    EXAM = "Экзамен"


@dataclass
class Event:
    event_date: date
    start_time: time
    end_time: time

@dataclass
class Lesson(Event):
    name: str
    cabinet: str
    teacher: str
    type: LessonType