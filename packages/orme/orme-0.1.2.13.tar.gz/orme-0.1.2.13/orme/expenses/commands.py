from datetime import date
from argparse import ArgumentParser, _SubParsersAction, _ArgumentGroup
from .run_expenses import (create_expense,
                           list_expenses,
                           update_expense,
                           delete_expense,
                           total)

from orme.constants import CATEGORIES

from orme.validations import validate_date


def run_create_expense(subparsers: _SubParsersAction):
    parser_add = subparsers.add_parser('add',
                                       help='adds a new expense with all its attributes',
                                       allow_abbrev=False)

    parser_add.add_argument('-v',
                            '--value',
                            type=int,
                            help='The  of this particular expense (not the register)',
                            required=True)
    parser_add.add_argument('-desc',
                            '--description',
                            type=str,
                            help='The description of this particular expense [optional]')
    parser_add.add_argument('-caty',
                            '--category',
                            type=str,
                            help='The category of the expense (default: food)',
                            choices=CATEGORIES,
                            default=CATEGORIES[0])
    parser_add.add_argument('-u',
                            '--user',
                            type=str,
                            help='Name of the user that generate the expense (default: Carlos)')
    parser_add.add_argument('--date',
                            type=validate_date,
                            help="""
                            The date when this expense ocurred in isoformat YYYY-MM-DD
                            (not the register date but the execute one)
                            - default: current day""",
                            default=date.today().isoformat())
    parser_add.add_argument('--div',
                            help='Whether this expense should be divided by 2 for calculation purposes',
                            action='store_true')

    parser_add.set_defaults(func=create_expense)


def run_list_expenses(subparsers: _SubParsersAction):
    parser_list = subparsers.add_parser('list',
                                        help='list expenses with filters',
                                        allow_abbrev=True)

    mutually_exclusive_by_value = parser_list.add_mutually_exclusive_group()
    mutually_exclusive_by_date = parser_list.add_mutually_exclusive_group()

    # In the future could be only a query command that is able to resolve every query db
    mutually_exclusive_by_value.add_argument('-gtv',
                                             '--greater-than-value',
                                             type=int,
                                             help='Filter by values greater than this one')
    mutually_exclusive_by_value.add_argument('-ltv',
                                             '--less-than-value',
                                             type=int,
                                             help='Filter by values less than this one')
    mutually_exclusive_by_value.add_argument('-btv',
                                             '--between-value',
                                             nargs=2,
                                             type=int,
                                             metavar=('start-value',
                                                      'end-value'),
                                             action='extend',
                                             help='Filter by the values provided (inclusive)')
    mutually_exclusive_by_value.add_argument('-eqv',
                                             '--equal-to-value',
                                             type=int,
                                             help="Filter by values equals to this one")
    mutually_exclusive_by_date.add_argument('-gtd',
                                            '--greater-than-date',
                                            type=validate_date,
                                            help='Filter by dates greater than this one')
    mutually_exclusive_by_date.add_argument('-ltd',
                                            '--less-than-date',
                                            type=validate_date,
                                            help='Filter by dates less than this one')
    mutually_exclusive_by_date.add_argument('-btd',
                                            '--between-date',
                                            nargs=2,
                                            type=validate_date,
                                            metavar=('start-date', 'end-date'),
                                            action='extend',
                                            help='Filter by the dates provided (inclusive)')
    mutually_exclusive_by_date.add_argument('-eqd',
                                            '--equal-to-date',
                                            type=validate_date,
                                            help="Filter by dates equals to this one")
    parser_list.add_argument('-caty',
                             '--category',
                             type=str,
                             help='Filter by this specific category')
    parser_list.add_argument('-u',
                             '--user',
                             type=str,
                             help='Filter by the specified user')
    parser_list.set_defaults(func=list_expenses)


def run_update_expenses(subparsers: _SubParsersAction):
    parser_update = subparsers.add_parser('update',
                                          help='Update the specified expense',
                                          allow_abbrev=False)

    parser_update.add_argument('--id',
                               type=str,
                               help='the id of the expense that needs to be updated',
                               required=True)
    parser_update.add_argument('-v',
                               '--value',
                               type=int,
                               help='The new value of this particular expense')
    parser_update.add_argument('-desc',
                               '--description',
                               type=str,
                               help='The description of this particular expense [optional]')
    parser_update.add_argument('-caty',
                               '--category',
                               type=str,
                               choices=CATEGORIES,
                               help='The category of the expense')
    parser_update.add_argument('-u',
                               '--user',
                               type=str,
                               help='Name of the user that generate the expense')
    parser_update.add_argument('--date',
                               type=validate_date,
                               help="The date when this expense ocurred in isoformat YYYY-MM-DD")
    parser_update.add_argument('--div',
                               help='Whether this expense should be divided for calculation purposes (0:False, 1:True)',
                               type=int,
                               choices=[0, 1],
                               dest='is_divided')
    parser_update.set_defaults(func=update_expense)


def run_delete_expense(subparsers: _SubParsersAction):
    parser_delete = subparsers.add_parser('delete',
                                          help='Delete the specified expense')

    parser_delete.add_argument('--id',
                               type=str,
                               help='The id of the expense to delete',
                               required=True)
    parser_delete.set_defaults(func=delete_expense)


def run_total(subparsers: _SubParsersAction):
    parser_total: ArgumentParser = subparsers.add_parser('total',
                                                         help='''Gets the count of all the expenses
                                                                 in the time frame specified''')

    mutually_exclusive_by_date: _ArgumentGroup = parser_total.add_mutually_exclusive_group()
    mutually_exclusive_by_date.add_argument('--between-date',
                                            type=validate_date,
                                            nargs=2,
                                            metavar=('start-date',
                                                     'end-date'),
                                            help='make the calculation based on the dates provided (inclusive)')

    mutually_exclusive_by_date.add_argument('--today',
                                            help='Gets the total expenses value of the current day',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('--yesterday',
                                            help='Gets the total expenses value of yesterday',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-lw',
                                            '--last-week',
                                            help='Get the total expenses value of the last week',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-cw',
                                            '--current-week',
                                            help='''Gets the total expenses value of the current week
                                                    (e.g monday - current day of the week)''',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-lm',
                                            '--last-month',
                                            help='Gets the total exxpenses value of the last month',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-cm',
                                            '--current-month',
                                            help='''Gets the total expenses value of the current month
                                                    (e.g 1 - current day of the month)''',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-ly',
                                            '--last-year',
                                            help='Gets the total expenses value of the last year',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('-cy',
                                            '--current-year',
                                            help='''Gets the total expenses value of the current year
                                                    (e.g 1 - current day of the year)''',
                                            action='store_true',
                                            default=None)
    mutually_exclusive_by_date.add_argument('--date',
                                            help="Get the total expenses value of the given date",
                                            type=validate_date)
    parser_total.set_defaults(func=total)
