from argparse import Namespace
from datetime import date
from typing import Tuple


TABLE_NAME = 'debts'


def generate_create_query(args: Namespace) -> Tuple[str, str]:
    today: str = date.today().isoformat()

    create_debts_table_query: str = f"""
    CREATE TABLE if not exists {TABLE_NAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        deptor TEXT,
        lender TEXT,
        description TEXT,
        interest_rate REAL NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
    """

    insert_into_debts_query = f"""
    INSERT INTO {TABLE_NAME}(
        value,
        deptor,
        lender,
        description,
        interest_rate,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.deptor}',
            '{args.lender}',
            '{args.description}',
            {args.interest_rate},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    return (create_debts_table_query, insert_into_debts_query)
