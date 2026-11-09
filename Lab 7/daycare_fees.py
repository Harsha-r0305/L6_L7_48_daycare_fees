import math


def parse_enrolment(text):
    """Parse 'age_group:hours' (e.g. 'toddler:25').

    Returns (AgeGroup, hours_as_float), or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:                      # missing or extra ':'
        return None
    age_group = parts[0].strip()
    if not age_group:                        # empty age group
        return None
    try:
        hours = float(parts[1])
    except (ValueError, OverflowError):      # non-numeric hours
        return None
    if not math.isfinite(hours) or hours < 0:    # reject nan, inf, negatives
        return None
    return age_group.title(), hours


def hours_average(hours_csv):
    """Average (floor) of comma-separated whole hours, e.g. '20,25,30'.

    Returns an int, or None if the input is invalid.
    """
    if not isinstance(hours_csv, str):
        return None
    values = []
    for item in hours_csv.split(','):
        item = item.strip()
        if not item:                         # empty element such as '1,,3' or ''
            return None
        try:
            value = int(item)
        except ValueError:                   # non-numeric / absurdly long number
            return None
        if value < 0:                        # negative hours make no sense
            return None
        values.append(value)
    return sum(values) // len(values)        # values is never empty here


def payable_fee(text):
    """Compute fee * 1.18 - discount from 'fee|discount' (e.g. '3000|250').

    Never returns a negative amount. Returns None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:                      # missing or extra '|'
        return None
    try:
        fee = float(parts[0])
        discount = float(parts[1])
    except (ValueError, OverflowError):
        return None
    if not (math.isfinite(fee) and math.isfinite(discount)):   # nan / inf
        return None
    if fee < 0 or discount < 0:              # negative fee or discount
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):             # overflow, e.g. 1e308 * 1.18
        return None
    return max(total, 0)


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result if result is not None else "Invalid input")

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
