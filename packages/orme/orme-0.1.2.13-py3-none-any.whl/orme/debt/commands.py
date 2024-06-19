from datetime import date

from .run_debt import (create_debt,
                       list_debts,
                       update_debt,
                       delete_debt)

from ..validations import validate_date


def run_create_debt(subparsers):
    parser_add = subparsers.add_parser('add',
                                       help='adds a new debt register whether the user is the debtor or the lender',
                                       allow_abbrev=False)
    # TODO: Read more about the names of the arguments (dest, metavar)
    parser_add.add_argument('-v',
                            '--value',
                            type=int,
                            help='The value of the dept',
                            required=True)
    parser_add.add_argument('-dpr',
                            '--deptor',
                            type=str,
                            help='The name of the deptor [optional]'
                            )
    parser_add.add_argument('-ld',
                            '--lender',
                            type=str,
                            help='The name of the lender [optional]')
    parser_add.add_argument('-desc',
                            '--description',
                            type=str,
                            help='A short description of the dept [optional]')
    parser_add.add_argument('-ir',
                            '--interest-rate',
                            type=float,
                            help='The interest rate monthly of the dept default 0.0',
                            default=0.00)
    parser_add.add_argument('--date',
                            type=validate_date,
                            help="""
                            Date of start of this particualr debt in isoformat YYYY-MM-DD
                            (not the register date but the execute one)
                            - default: current day""",
                            default=date.today().isoformat())

    parser_add.set_defaults(func=create_debt)


def run_list_debts(subparsers):
    parser_list = subparsers.add_parser('list',
                                        help='list depts with or without filteres')

    mutually_exclusive_by_value = parser_list.add_mutually_exclusive_group()
    mutually_exclusive_by_date = parser_list.add_mutually_exclusive_group()

    mutually_exclusive_by_value.add_argument('-gtv',
                                             '--greater-than-value',
                                             type=int,
                                             help='Filter by values greater than this one (inclusive)')
    mutually_exclusive_by_value.add_argument('-ltv',
                                             '--lower-than-value',
                                             type=int,
                                             help='Filter by values lower than this one (inclusive)')
    mutually_exclusive_by_value.add_argument('-eqv',
                                             '--equal-to-value',
                                             type=int,
                                             help='Filter by values equal to this one')
    mutually_exclusive_by_value.add_argument('-btv',
                                             '--between-values',
                                             nargs=2,
                                             metavar=('value-start',
                                                      'value-end'),
                                             type=int,
                                             help='Filter by values between the values provided (inclusive)',
                                             action='extend')
    mutually_exclusive_by_date.add_argument('-gtd',
                                            '--greater-than-date',
                                            type=validate_date,
                                            help='Filter by dates greater than this one (inclusive)')
    mutually_exclusive_by_date.add_argument('-ltd',
                                            '--lower-than-date',
                                            type=validate_date,
                                            help='Filter by dates lower than this one (inclusive)')
    mutually_exclusive_by_date.add_argument('-eqd',
                                            '--equal-to-date',
                                            type=validate_date,
                                            help='Filter by dates equal to this one')
    mutually_exclusive_by_date.add_argument('-btd',
                                            '--between-dates',
                                            nargs=2,
                                            metavar=('date-start', 'date-end'),
                                            type=validate_date,
                                            help='Filter by dates between the dates provided (inclusive)',
                                            action='extend')

    parser_list.set_defaults(func=list_debts)


def run_update_debt(subparsers):
    parser_update = subparsers.add_parser('update',
                                          help="Update the specified debt",
                                          allow_abbrev=False)

    parser_update.add_argument('--id',
                               type=str,
                               help='The id of the debt to be updated',
                               required=True)
    parser_update.add_argument('-v',
                               '--value',
                               type=int,
                               help='The value of the dept')
    parser_update.add_argument('-dpr',
                               '--deptor',
                               type=str,
                               help='The name of the deptor [optional]'
                               )
    parser_update.add_argument('-ld',
                               '--lender',
                               type=str,
                               help='The name of the lender [optional]')
    parser_update.add_argument('-desc',
                               '--description',
                               type=str,
                               help='A short description of the dept [optional]')
    parser_update.add_argument('-ir',
                               '--interest-rate',
                               type=float,
                               help='The interest rate monthly of the dept')
    parser_update.add_argument('--date',
                               type=validate_date,
                               help='Date of start of this particualr debt in isoformat YYYY-MM-DD')

    parser_update.set_defaults(func=update_debt)


def run_delete_debt(subparsers):
    parser_delete = subparsers.add_parser('delete',
                                          help='Delete the specified debt')

    parser_delete.add_argument('--id',
                               help='The id of the debt to be deleted')

    parser_delete.set_defaults(func=delete_debt)
