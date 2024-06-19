import calendar
from datetime import date, timedelta
from typing import List, Tuple


def generate_dateframe(args: List[Tuple[str, str]]) -> List[Tuple[str, str | List[str]]]:
    local_args: List[Tuple[str, str | List[str]]] = []
    dateframe: str | List[str] = ''
    SUNDAY = 6

    match args:
        case [('today', _)]:
            dateframe = date.today().isoformat()
            local_args = [('equal-to-date', dateframe)]
        case [('yesterday', _)]:
            dateframe = date.today() - timedelta(days=1)
            local_args = [('equal-to-date', dateframe)]
        case[('date', date_)]:
            dateframe = date_
            local_args = [('equal-to-date', dateframe)]
        case [(arg, _)] if arg.startswith('last'):
            match arg:
                case arg if arg.endswith('week'):
                    last_week_date = date.today() - timedelta(weeks=1)
                    last_week_start_date = last_week_date - timedelta(days=last_week_date.weekday())
                    last_week_last_date = last_week_date + timedelta(days=(SUNDAY - last_week_date.weekday()))

                    dateframe = [last_week_start_date.isoformat(), last_week_last_date.isoformat()]
                case arg if arg.endswith('month'):
                    last_month_date = date.today() - timedelta(weeks=4)
                    last_month: int = last_month_date.month
                    year_of_month: int = last_month_date.year
                    last_month_last_day: int = calendar.monthrange(year_of_month, last_month)[1]
                    last_month_start_date: str = date(year_of_month, last_month, 1).isoformat()
                    last_month_last_date: str = date(year_of_month, last_month, last_month_last_day).isoformat()

                    dateframe = [last_month_start_date, last_month_last_date]
                case arg if arg.endswith('year'):
                    last_year: int = date.today().year - 1

                    last_year_start_date: str = date(last_year, 1, 1).isoformat()
                    last_year_last_date: str = date(last_year, 12, 31).isoformat()

                    dateframe = [last_year_start_date, last_year_last_date]

            local_args = [('between-date', dateframe)]
        case [(arg, _)] if arg.startswith('current'):
            match arg:
                case arg if arg.endswith('week'):
                    current_week_start_date: date = date.today() - timedelta(days=date.today().weekday())
                    current_week_last_date: date = date.today() + timedelta(days=(SUNDAY - date.today().weekday()))

                    dateframe = [current_week_start_date.isoformat(), current_week_last_date.isoformat()]
                case arg if arg.endswith('month'):
                    current_month: int = date.today().month
                    current_year: int = date.today().year

                    current_month_last_day: int = calendar.monthrange(current_year, current_month)[1]
                    current_month_start_date: str = date(current_year, current_month, 1).isoformat()
                    current_month_last_date: str = date(current_year, current_month, current_month_last_day).isoformat()

                    dateframe = [current_month_start_date, current_month_last_date]
                case arg if arg.endswith('year'):
                    current_year: int = date.today().year

                    current_year_start_date: str = date(current_year, 1, 1).isoformat()
                    current_year_last_date: str = date(current_year, 12, 31).isoformat()

                    dateframe = [current_year_start_date, current_year_last_date]

            local_args = [('between-date', dateframe)]
        case _:
            # A full query is perform
            return []

    return local_args
