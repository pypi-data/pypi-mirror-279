# Orme

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

Orme is a command-line interface (CLI) application and it is in early stages of development, it is intended to keep track of personal expenses and debts, in order to be able to have insights about personal financial situation such as, how much is the user expending in different time frames (weeks, months, years), what are the things in which the user expends more its money (food, bills, clothes, etc), as well as what debts the user has, or which of them the user is actually the lender.

Orme is currently changing and the objective is to add graphical information through several charts which help the user have a better view of all the information related to expenses, debts and investments.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Installation

### Prerequisites

- Python 3.x

### Installation Steps

1. Create a virtual environment (optional but recommended since it is an alpha version):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the app directly from TestPyPI:

    ```sh
    pip install --extra-index-url https://testpypi.python.org/pypi orme=={version} # Current tested version 0.1.2.13
    ```
..
## Usage

Orme has 2 types of registers to be added and both of them have different arguments and options, you can always use the --help option to get information for each command.

```sh
usage: Orme [-h] [-v] {expenses,debts} ...

This program allows the user to manage the expenses, incomes and other financial situations

options:
  -h, --help        show this help message and exit
  -v, --version     Gives the version of the package

[commands]:
  {expenses,debts}
    expenses        Executes all operations related to expenses
    debts           Executes all operations related to debt
```

### Register an expense

To register an expense you can use the following command:

```sh
orme expenses add --value 5000 --description 'I did some shoping at the store' --category 'food' --date '2024-06-11'
```

The `--date` option is optional and if not specified the current date would be selected, note that the date specified must be in ISOfomrat `YYYY-MM-DD`, use this option if the expense you are registering does not happend in the current day. Categories are already define and you can specified a category which is either of these options `{food,home,bills,technologic,travel,clothes,other}`, categories could be parametrize by users and I am analizing that posibility, `--category` is also optional and if not specified the first option `(food)` would be selected.

### Listing expenses

The basic way to list your registered expenses is using the following command:

```sh
orme expenses list
```

This will list your expenses in a paginated way from the most recent date to the most distant one, which means that the expenses will be shown from 10 to 10, to continue the pagination you have to press the `ENTER` key and to stop the pagination you have to press the `q` key, `CTRL + C` can also stop it. You can specified options `(value and/or date)` with the combinations `(<=, =, =>)`, this could end up in a list of expenses that happened in an interval of dates and with a specified value, here are some examples:

#### Listing expenses by date

#### (equal to date)

```sh
orme expenses list -etd '2024-06-11'
```

#### (greater than date)

```sh
orme expenses list -gtd '2024-06-11'
```

#### (less than date)

```sh
orme expenses list -ltd '2024-06-11'
```

#### (between dates)

```sh
orme expenses list -btd '2024-06-11' '2024-06-18'
```

You can replicate this for the `value` option

### Getting total value of expenses

The user can also get the total value of the expenses that happend in different range of dates, orme simplifies some options so the user can specified range dates easily being these options `(today, yesterday, last-week, current-week, last-month, current-month, last-year, current-year)`, specifiyng `between-date` and `date` is also possible if the user want a different range date from the ones provided or the total value for a single date.

#### Getting the total value of expenses

#### (today)

```sh
orme expenses total --today
```

#### (yesterday)

```sh
orme expenses total --yesterday
```

#### (current-month)

```sh
orme expenses total --current-month
```

#### (last-year)

```sh
orme expenses total --last-year
```

#### (custom range dates)

```sh
orme expenses total --between-date '2023-01-12' '2024-05-12'
```

#### (specific date)

```sh
orme expenses total --date '2024-06-12'
```

### updating expenses

You can as well update your expenses specifiyng the `id` and the fields you want to update like this:

```sh
orme expenses update --id {your_expense_id} --{field_to_update} {new_value} #(value, description, date, category)
```

### deleting expenses

To delete expenses you just have to specify the `id`:

```sh
orme expenses delete --id {your_expense_id}
```

### registering debts

For now debts only allows a simple CRUD operation, I have more things in mind to this feature but lets see what the user can do for now starting with a simple insertion. if you type the `help` command you get the following:

```sh
usage: Orme debts add [-h] -v VALUE [-dpr DEPTOR] [-ld LENDER] [-desc DESCRIPTION] [-ir INTEREST_RATE] [--date DATE]

options:
  -h, --help            show this help message and exit
  -v VALUE, --value VALUE
                        The value of the dept
  -dpr DEPTOR, --deptor DEPTOR
                        The name of the deptor [optional]
  -ld LENDER, --lender LENDER
                        The name of the lender [optional]
  -desc DESCRIPTION, --description DESCRIPTION
                        A short description of the dept [optional]
  -ir INTEREST_RATE, --interest-rate INTEREST_RATE
                        The interest rate monthly of the dept default 0.0
  --date DATE           Date of start of this particualr debt in isoformat YYYY-MM-DD (not the register date but the
                        execute one) - default: current day
```

Despite `lender` and `deptor` being optional, I highly recommend you to get well define these fields, here is a simple example:

```sh
orme debts add --value 100000 --deptor 'Esteban' --lender 'Maria' --description 'Por que Maria!' --date '2024-05-01'
```

### Listing debts

Listing debts is pretty much the same as listing expenses, here are some examples:

```sh
orme debts list
```

#### Listing expenses by date

#### (equal to date)

```sh
orme debts list -etd '2024-06-11'
```

#### (greater than date)

```sh
orme debts list -gtd '2024-06-11'
```

It would be the same for updating and deleting debts

### updating debts

```sh
orme expenses update --id {your_expense_id} --{field_to_update} {new_value} #(value, description, date, category)
```

### deleting debts

```sh
orme expenses delete --id {your_expense_id}
```

## Contact

Feel free to contact me if you have some suggestions or feedback

### Email
 - carlosdcorrea3@gmail.com

### Linkedin
 - https://www.linkedin.com/in/carlos-correa-1ba7861b8/