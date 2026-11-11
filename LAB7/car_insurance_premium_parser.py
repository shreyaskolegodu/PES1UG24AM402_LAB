"""Defensive parsers: invalid registrations return ''; invalid numbers/dates return None."""
from datetime import date
import re


def normalize_registration(plate):
    if not isinstance(plate, str):
        return ""
    return ''.join(ch for ch in plate.strip().upper() if not ch.isspace() and ch not in '-.')


def total_claim_amount(text):
    """Sum nonnegative ASCII integer amounts; reject the whole malformed record."""
    if not isinstance(text, str) or not text.strip():
        return None
    parts = [part.strip() for part in text.split(';')]
    if any(not re.fullmatch(r'[0-9]{1,100}', part) for part in parts):
        return None
    return sum(int(part) for part in parts)


def driver_age(dob, current_year=2026):
    """Calendar-year age (the original contract), or None for an invalid date/year."""
    if not isinstance(dob, str) or type(current_year) is not int or not 1 <= current_year <= 9999:
        return None
    match = re.fullmatch(r'([0-9]{2})/([0-9]{2})/([0-9]{4})', dob.strip())
    if match is None:
        return None
    day, month, year = map(int, match.groups())
    try:
        date(year, month, day)
    except ValueError:
        return None
    return current_year - year if year <= current_year else None


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    print("Driver age in 2026:", driver_age(value))

if __name__ == "__main__":
    main()

