import sqlite3
from sqlite3 import Cursor, Connection
from typing import List, Tuple, Union

from pandas import DataFrame


def create(cur: Cursor, con: Connection, queries: List[str], table_name: str) -> None:
    create_table_query = queries[0]
    insert_into_query = queries[1]

    cur.execute(create_table_query)
    cur.execute(insert_into_query)
    con.commit()
    cur.close()

    print(f'Register created in table {table_name} successfully')


def list_(cur: Cursor, queries: List[str], table_name: str) -> None:
    query_results = queries[0]
    query_count = queries[1]

    get_table_columns_query = f'PRAGMA table_info({table_name})'
    offset: int = 0
    try:
        cur.execute(get_table_columns_query, ())
        columns: List[Tuple[Union[int, str]]] = cur.fetchall()

        cur.execute(query_count)
        count: int = cur.fetchone()[0]

        if not count:
            print('No data found')
            return

        limit: int = 10 if count > 10 else count
        remaining: int = 0 if not (count - limit) else count - limit

        print(
            f'number of register for this query in table {table_name} {count}')

        while True:
            # print('starting with offset {} and limit {} and remaining {}'.format(offset, limit, remaining))
            # TODO: use pandas sql reader instead of cur to retrieve the rows
            # get the requested data
            cur.execute(query_results, (offset, limit))
            results: List[Tuple[Union[str, int]]] = cur.fetchall()

            df = DataFrame.from_records(data=results,
                                        columns=[column[1] for column in columns])

            if df.empty and not offset:
                print('Nothing to show')
                return
            elif df.empty:
                print('Nothing more to show')
                return

            print(df)

            while True:
                try:
                    user_input = input(f'({remaining}):')
                except KeyboardInterrupt:
                    return
                if user_input == 'q':
                    return
                elif user_input == '':
                    break
                else:
                    continue

            offset, limit = offset + limit, remaining if remaining < limit else limit
            remaining -= limit
            # print('finishing with offset {} and limit {} and remaining {}'.format(offset, limit, remaining))

    except sqlite3.OperationalError as e:
        error = f'We can\'t perform this action because the table {table_name} does not exists'
        print('This is the real error')
        print(e)
        print(f'error {error}')
        cur.close()


def update(cur: Cursor, con: Connection, queries: List[str]) -> None:
    update_query = queries[0]
    cur.execute(update_query)
    con.commit()

    if cur.rowcount:
        print('Registro actualizado satisfactoriamente')
    else:
        print('No register found with the specified id')

    cur.close()


def delete(cur: Cursor, con: Connection, queries: List[str]) -> None:
    delete_query = queries[0]

    cur.execute(delete_query)
    con.commit()

    if cur.rowcount > 0:
        print('Register deleted')
    else:
        print('No registers found to delete')

    cur.close()


def total(cur: Cursor, queries: List[str]) -> None:
    total_expenses_value_query: str = queries[0]
    count_registers: str = queries[1]

    # print(total_expenses_value_query)
    # print(count_registers)
    cur.execute(total_expenses_value_query)
    result: int | None = cur.fetchone()[0]

    cur.execute(count_registers)
    count: int = cur.fetchone()[0]

    if count:
        print(f'{count} expenses found with a total value of {result}')
        return

    print('No data found')
