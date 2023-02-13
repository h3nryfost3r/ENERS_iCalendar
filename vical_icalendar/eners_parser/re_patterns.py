import re

RE_DATE = re.compile(r'(\d*)-(\d*)-(\d*)', re.M)
RE_TIME = re.compile(r'((\d{2}):(\d{2})) ((\d{2}):(\d{2}))', re.M)
RE_LESSON = re.compile(r'(л\.|пр\.|лаб\.|экзамен)\s+([А-Яа-я ]+)', re.M)
RE_CABINET = re.compile(r'\n(\D-(\d{3}|\d{3}\(\d\)|\d{3}\w))\n', re.M)
RE_TEACHER = re.compile(r'\n\n([\w.]*.\. \w*. \w\.\w\.)', re.M)
