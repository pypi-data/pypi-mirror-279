from argparse import Namespace
from datetime import date
from typing import Tuple


TABLE_NAME = 'expenses'


def generate_create_query(args: Namespace) -> Tuple[str, str]:
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

    create_expenses_table_query = f"""
    CREATE TABLE if not exists {TABLE_NAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        user TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        is_divided INTEGER NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
    """

    insert_into_expenses_query = f"""
    INSERT INTO {TABLE_NAME}(
        value,
        user,
        category,
        description,
        is_divided,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.user}',
            '{args.category}',
            '{args.description}',
            {is_divided},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    return (create_expenses_table_query, insert_into_expenses_query)
