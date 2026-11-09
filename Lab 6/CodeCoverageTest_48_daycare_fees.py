import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status

def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_unknown_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("teenager", 10, False)

def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("infant", -1, False)

def test_sibling_discount_adds_included_hours():
    assert extra_hours_fee("preschool", 40, True) == 45

def test_infant_standard_rate():
    assert extra_hours_fee("infant", 30, False) == 140

def test_toddler_high_extra_surcharge():
    assert extra_hours_fee("toddler", 50, False) == 25 * 14

def test_infant_high_extra_surcharge():
    assert extra_hours_fee("infant", 45, False) == 25 * 22

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_too_young():
    assert enrolment_allowed(3, 5, False) is False

def test_enrolment_immunisation_pending_old_enough():
    assert enrolment_allowed(18, 1, True) is True

def test_pickup_on_time():
    assert pickup_status(15, False, False) == "on_time"

def test_pickup_late():
    assert pickup_status(5, False, False) == "late"

def test_pickup_overdue_aftercare_friday():
    assert pickup_status(0, True, True) == "overdue"
