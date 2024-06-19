import pytest

from ..orme.validations import validate_date


def test_validate_date():
    """
    While the execution of this tests i realize that the
    expression assert validate_date('20240120') is None
    returns an error due to the venv python interpreter 3.10.10
    when tested the method with the python interpreter 3.11.3
    it works just fine"""
    assert validate_date('2024-01-20') is None

    with pytest.raises(SystemExit):
        validate_date('2024-20-01')

    with pytest.raises(SystemExit):
        validate_date('20242001')

    with pytest.raises(SystemExit):
        validate_date('2024/20/01')

    with pytest.raises(SystemExit):
        validate_date('20240120')

    with pytest.raises(SystemExit):
        validate_date('01302024')
