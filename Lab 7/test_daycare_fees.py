import math

from hypothesis import given, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee


# ---------- 1. "Must never crash" fuzz tests (random text and None) ----------
@given(st.text() | st.none())
def test_parse_enrolment_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:
        assert False, f"parse_enrolment crashed with: {e!r}"


@given(st.text() | st.none())
def test_hours_average_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:
        assert False, f"hours_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"


# ---------- 2. Property tests on the *values* returned ----------
@given(st.text() | st.none() | st.integers() | st.floats())
def test_non_string_or_garbage_never_crashes_any_function(s):
    for fn in (parse_enrolment, hours_average, payable_fee):
        try:
            fn(s)
        except Exception as e:
            assert False, f"{fn.__name__} crashed with: {e!r}"


@given(st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1),
       st.floats(min_value=0, max_value=1e6))
def test_parse_enrolment_valid_input_roundtrip(group, hours):
    result = parse_enrolment(f"{group}:{hours}")
    if group.strip():
        assert result is not None
        assert result[1] == hours
        assert result[0] == group.strip().title()


@given(st.lists(st.integers(min_value=0, max_value=168), min_size=1))
def test_hours_average_within_min_and_max(values):
    avg = hours_average(",".join(map(str, values)))
    assert avg is not None
    assert min(values) <= avg <= max(values)


@given(st.floats(min_value=0, max_value=1e9),
       st.floats(min_value=0, max_value=1e9))
def test_payable_fee_never_negative_and_finite(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert result >= 0
    assert math.isfinite(result)


def test_known_examples():
    assert parse_enrolment("toddler:25") == ("Toddler", 25.0)
    assert hours_average("20,25,30") == 25
    assert payable_fee("3000|250") == 3000 * 1.18 - 250
    assert payable_fee("100|500") == 0
