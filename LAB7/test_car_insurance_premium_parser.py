from hypothesis import given, settings, strategies as st
from car_insurance_premium_parser import normalize_registration, total_claim_amount, driver_age

@settings(max_examples=500, derandomize=True, deadline=None)
@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    try:
        result = normalize_registration(s)
    except Exception as e:
        assert False, f"normalize_registration crashed with {s!r}: {e}"
    assert isinstance(result, str)

@settings(max_examples=500, derandomize=True, deadline=None)
@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    try:
        result = total_claim_amount(s)
    except Exception as e:
        assert False, f"total_claim_amount crashed with {s!r}: {e}"
    assert result is None or (isinstance(result, int) and result >= 0)

@settings(max_examples=500, derandomize=True, deadline=None)
@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    try:
        result = driver_age(s)
    except Exception as e:
        assert False, f"driver_age crashed with {s!r}: {e}"
    assert result is None or (isinstance(result, int) and result >= 0)
