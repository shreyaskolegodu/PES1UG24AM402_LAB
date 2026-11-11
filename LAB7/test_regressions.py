import pytest
from hypothesis import given, strategies as st
from car_insurance_premium_parser import normalize_registration, total_claim_amount, driver_age

@pytest.mark.parametrize('value', [None, 42, [], {}, True, 1.2, b'abc'])
def test_non_strings(value):
    assert normalize_registration(value) == ''
    assert total_claim_amount(value) is None
    assert driver_age(value) is None

@pytest.mark.parametrize('value', ['', '1;;3', '-1', '1.2', 'one', '9'*101, '²'])
def test_invalid_claims(value):
    assert total_claim_amount(value) is None

@pytest.mark.parametrize('value', ['', '31/02/2000', '29/02/1900', '01/13/2000', '01/01/2027', '1/1/2000'])
def test_invalid_dates(value):
    assert driver_age(value) is None

def test_valid_examples():
    assert normalize_registration(' ka-01.ab 1234 ') == 'KA01AB1234'
    assert total_claim_amount('12000;4500;800') == 17300
    assert total_claim_amount(' 0 ; 20 ') == 20
    assert driver_age('29/02/2000') == 26
    assert driver_age('14/08/1999') == 27
    assert driver_age('01/01/2000', None) is None

@given(st.lists(st.integers(min_value=0,max_value=10**12), min_size=1,max_size=30))
def test_claim_sum(amounts):
    assert total_claim_amount(';'.join(map(str,amounts))) == sum(amounts)

@given(st.dates(min_value=__import__('datetime').date(1,1,1),max_value=__import__('datetime').date(2026,12,31)))
def test_valid_date_age(d):
    assert driver_age(f'{d.day:02}/{d.month:02}/{d.year:04}') == 2026-d.year

@given(st.text())
def test_normalization_idempotent(s):
    assert normalize_registration(normalize_registration(s)) == normalize_registration(s)
