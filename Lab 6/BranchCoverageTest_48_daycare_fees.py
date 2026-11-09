import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status

def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("teenager", 10, False)

def test_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("infant", -1, False)

def test_zero_hours_is_valid():
    assert extra_hours_fee("infant", 0, False) == 0

def test_sibling_discount_non_infant():
    assert extra_hours_fee("preschool", 40, True) == 45

def test_sibling_no_discount_for_infant():
    assert extra_hours_fee("infant", 30, True) == 140

def test_no_sibling_non_infant():
    assert extra_hours_fee("toddler", 30, False) == 45

def test_exactly_at_included_limit():
    assert extra_hours_fee("preschool", 30, False) == 0

def test_extra_exactly_20_no_surcharge():
    assert extra_hours_fee("toddler", 45, False) == 20 * 9

def test_extra_21_toddler_surcharge():
    assert extra_hours_fee("toddler", 46, False) == 21 * 14

def test_extra_21_infant_surcharge():
    assert extra_hours_fee("infant", 41, False) == 21 * 22

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_too_young():
    assert enrolment_allowed(5, 5, False) is False

def test_enrolment_exactly_six_months_with_vacancy():
    assert enrolment_allowed(6, 1, False) is True

def test_enrolment_no_vacancy():
    assert enrolment_allowed(24, 0, False) is False

def test_immunisation_pending_exactly_12_months():
    assert enrolment_allowed(12, 0, True) is True

def test_immunisation_pending_under_12_months():
    assert enrolment_allowed(11, 5, True) is False

def test_pickup_on_time_regular():
    assert pickup_status(10, False, False) == "on_time"

def test_pickup_late_regular():
    assert pickup_status(-5, False, False) == "late"

def test_pickup_overdue_regular():
    assert pickup_status(-6, False, False) == "overdue"

def test_pickup_on_time_aftercare():
    assert pickup_status(20, True, False) == "on_time"

def test_pickup_late_aftercare():
    assert pickup_status(19, True, False) == "late"

def test_pickup_friday_regular_on_time():
    assert pickup_status(20, False, True) == "on_time"

def test_pickup_friday_aftercare_late_and_overdue():
    assert pickup_status(15, True, True) == "late"
    assert pickup_status(14, True, True) == "overdue"
