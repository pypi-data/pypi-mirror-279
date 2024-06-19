import argparse
from argparse import ArgumentParser, _SubParsersAction

from orme import __app_name__, __version__

from .debt.commands import (run_create_debt,
                            run_list_debts,
                            run_update_debt,
                            run_delete_debt)

from .expenses.commands import (run_create_expense,
                                run_list_expenses,
                                run_update_expenses,
                                run_delete_expense,
                                run_total)


def run_options(subparsers: _SubParsersAction) -> None:
    parser_expenses: ArgumentParser = subparsers.add_parser('expenses',
                                                            help='Executes all operations related to expenses')
    parser_debts: ArgumentParser = subparsers.add_parser('debts',
                                                         help='Executes all operations related to debt')

    subparser_expenses: _SubParsersAction[ArgumentParser] = parser_expenses.add_subparsers(
        title='[sub-commands]')
    subparser_debts:  _SubParsersAction[ArgumentParser] = parser_debts.add_subparsers(
        title='[sub-commands]')

    run_create_expense(subparser_expenses)
    run_list_expenses(subparser_expenses)
    run_update_expenses(subparser_expenses)
    run_delete_expense(subparser_expenses)
    run_total(subparser_expenses)

    run_create_debt(subparser_debts)
    run_list_debts(subparser_debts)
    run_update_debt(subparser_debts)
    run_delete_debt(subparser_debts)


def main():
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="Orme",
        description="""
                     This program allows the user to manage the expenses,
                     incomes and other financial situations
                     """,
        epilog="TechSsus - Carlos Correa"
    )

    # QUESTION: Support localization?
    parser.add_argument(
        '-v',
        '--version',
        help='Gives the version of the package',
        action='version',
        version=f'{__app_name__} version: {__version__}'
    )

    # REFACTOR: Commands should go 'expenses list' instead of 'list expenses'
    subparsers_options: _SubParsersAction[ArgumentParser] = parser.add_subparsers(
        title='[commands]')

    run_options(subparsers_options)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.parse_args(['--h'])
