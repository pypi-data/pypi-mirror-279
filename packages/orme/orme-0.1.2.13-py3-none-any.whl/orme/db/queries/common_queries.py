from datetime import date
from typing import List, Tuple

from orme.db.common import generate_sql_where_by_operator
from orme.expenses.utils import generate_dateframe


def generate_list_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str, str]:
    where_statement: str = ''

    if args:
        where_statement = generate_sql_where_by_operator(args)

    query_results = f"""
                    SELECT * FROM {table_name}
                    {where_statement}
                    ORDER BY date DESC
                    LIMIT ?, ?
                    """

    query_count = f"""
                   SELECT COUNT(*)
                   FROM {table_name}
                   {where_statement}
                   """

    return (query_results, query_count)


def generate_update_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str]:
    today = date.today().isoformat()

    update_table_query = f"""
    UPDATE {table_name}
    SET {", ".join(
        [" = ".join(
            [f"'{item}'" for item in arg])
                         for arg in args[1:]])}, updated = '{today}'
    WHERE {" = ".join([str(item) for item in args[0]])}"""

    return (update_table_query,)


def generate_delete_query(args: List[Tuple[str, str | int]], table_name) -> Tuple[str]:
    delete_expense_query = f"""
    DELETE FROM {table_name}
    WHERE {"=".join([item for item in args[0]])}"""

    return (delete_expense_query,)


def generate_total_query(args: List[Tuple[str, str]], table_name) -> Tuple[str]:
    local_args: List[Tuple[str, str | List[str]]] = generate_dateframe(args)
    where_statement: str = ''

    if local_args:
        where_statement = generate_sql_where_by_operator(local_args)

    total_expenses_value_query: str = f"""
    SELECT SUM(value) FROM {table_name}
    {where_statement}"""

    count_registers: str = f"""
    SELECT COUNT(*)
    FROM {table_name}
    {where_statement}"""

    return (total_expenses_value_query, count_registers)
