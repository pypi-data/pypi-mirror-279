from typing import List, Tuple


def generate_sql_where_by_operator(args: List[Tuple[str, str | int]]) -> str:
    where_statement = 'WHERE '
    common_operators = ['<=', '>=', '=']

    for arg in args:
        print(arg)
        if where_statement != 'WHERE ':
            where_statement += 'AND'

        operator = get_operator(arg[0])
        field = get_field_name(arg[0])

        values: str | int | List[str | int] = arg[1]
        if operator in common_operators:
            if isinstance(values, str):
                values = f"'{values}'"
            where_statement += f'{field} {operator} {values}'
        elif operator == '><':
            if isinstance(values[0], str):
                values[0], values[1] = f"'{values[0]}'", f"'{values[1]}'"
            where_statement += f"{field} BETWEEN {values[0]} AND {values[1]}"
    return where_statement


def get_operator(arg: str) -> str | None:
    match arg:
        case arg if arg.startswith('between'):
            return '><'
        case arg if arg.startswith('greater'):
            return '>='
        case arg if arg.startswith('less'):
            return '<='
        case arg if arg.startswith('equal'):
            return '='
        case _:
            return None


def get_field_name(arg: str) -> str | None:
    match arg:
        case arg if arg.endswith('value'):
            return 'value'
        case arg if arg.endswith('date'):
            return 'date'
        case _:
            return None
