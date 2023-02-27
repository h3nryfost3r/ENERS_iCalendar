import time
from typing import Optional, List

import typer

from yaspin import yaspin

from vical_icalendar.parser_handler import schemas
from vical_icalendar.response_handler.init_response import InitResponse
from vical_icalendar.parser_handler.parser import ParserHandler
from vical_icalendar.calendar_handler.calendar import ICalendarHandler

app = typer.Typer()

@app.command(
    help="Создает iCalendar файл для дальнейшего импорта в календарь"
)
def create(
        group_name = typer.Argument(
            ..., help="Название вашей группы (Пример: ТРП-3-20)"),
        path_name: str = typer.Argument(
            default='file.ics', help='Путь к файлу .ics'),
        is_month: Optional[bool] = typer.Option(
            True, "--month/--week", help="события месяца или недели"),
        is_next: Optional[bool] = typer.Option(
            False, "--next/--current", help="события текущего/следующего месяца/недели")
):
    weeks_range: range
    with yaspin(text="Creating init response. Getting range of ENERS weeks", color="blue") as spinner:
        init_response = InitResponse(
            group_name=group_name,
            is_month=is_month,
            is_week=not is_month,
            is_next=is_next
        )
        if any(weeks_range := init_response.get_weeks_range()):
            spinner.ok("OK >")
        else:
            spinner.fail("Failed! [X]")

    events: List[schemas.Lesson]
    with yaspin(text="Getting events from responses", color="blue") as spinner:
        parser = ParserHandler(
            group_name=group_name,
            weeks_range=weeks_range,
            is_month=is_month,
            is_next=is_next
        )
        if any(events := parser.get_lessons()):
            spinner.ok("OK >")
        else:
            spinner.fail("Failed! [X]")

    vical_calendar: ICalendarHandler
    with yaspin(text=f"Writing your {path_name} file", color="blue") as spinner:
        vical_calendar = ICalendarHandler(data=events)
        write_status = vical_calendar.write_ical(path_name)
        if write_status:
            spinner.ok("OK >")
        else:
            spinner.fail("Failed! [X]")



if __name__ == "__main__":
    app()