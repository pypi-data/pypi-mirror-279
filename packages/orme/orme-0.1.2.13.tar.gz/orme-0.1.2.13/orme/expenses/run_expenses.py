from argparse import Namespace
from typing import Tuple, List

from orme.utils import get_present_arguments

from orme.db.connection import create_connection_and_execute_query
from orme.settings import (QUERY_CREATE,
                           QUERY_LIST,
                           QUERY_UPDATE,
                           QUERY_DELETE)
from orme.db.queries.queries_expenses import generate_create_query
from orme.db.queries.common_queries import (generate_list_query,
                                            generate_update_query,
                                            generate_delete_query,
                                            generate_total_query)


TABLE_NAME = 'expenses'
QUERY_TOTAL = 5


def define_query(query_type: int, args: Namespace) -> str:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = []

    if query_type == QUERY_CREATE:
        queries = generate_create_query(args)
    if query_type == QUERY_LIST:
        queries = generate_list_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_UPDATE:
        if len(present_arguments) == 1:
            raise ValueError('This command requires the fields to be updated')
        queries = generate_update_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_DELETE:
        queries = generate_delete_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_TOTAL:
        queries = generate_total_query(present_arguments, TABLE_NAME)

    return queries


def create_expense(args: Namespace) -> None:
    create_connection_and_execute_query(
        'create', define_query(QUERY_CREATE, args), TABLE_NAME)


def list_expenses(args: Namespace) -> None:
    create_connection_and_execute_query(
        'list', define_query(QUERY_LIST, args), TABLE_NAME)


def update_expense(args: Namespace) -> None:
    try:
        create_connection_and_execute_query(
            'update', define_query(QUERY_UPDATE, args), TABLE_NAME)
    except ValueError as e:
        print(e)


def delete_expense(args: Namespace) -> None:
    create_connection_and_execute_query(
        'delete', define_query(QUERY_DELETE, args), TABLE_NAME)


def total(args: Namespace) -> None:
    create_connection_and_execute_query(
        'total', define_query(QUERY_TOTAL, args), TABLE_NAME)
