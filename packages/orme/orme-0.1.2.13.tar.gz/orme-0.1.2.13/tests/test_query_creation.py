from orme.debt.run_debt import generate_list_query


def test_generate_list_query_debt():
    TABLE_NAME = 'debts'

    assert_string_query_where: str = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE date == 5/07/2024
    ORDER BY date DESC
    LIMIT 0, 10
    """

    generate_list_query()