# Lab 7 - Fuzzing for Input Validation Bugs
Shreyas K M | PES1UG24AM402

Source: https://github.com/SETAPESU26/L6_L7_55_car_insurance_premium (snapshot 0ef1e60ba3890bc9b75430ab07010cd1a3a151f5).

## Run fixed implementation
```sh
python -m pip install -r requirements.txt
python car_insurance_premium_parser.py
python -m pytest test_car_insurance_premium_parser.py test_regressions.py -q
```
Result: 27 passing tests, including three required no-crash properties with up to 500 deterministic examples each. `test_regressions.py` adds invalid-type, malformed claims, calendar/date validation and semantic property checks.

## Reproduce original failures without modifying fixed code
Copy `original/car_insurance_premium_parser.py` and `test_car_insurance_premium_parser.py` to a temporary directory. From that directory run:
```sh
python -m pytest test_car_insurance_premium_parser.py --tb=short -q
```
Expected: three failing tests. Hypothesis reduces failures to None and empty strings. The original source is retained exactly.

## Application evidence (SS1 and SS3)
Run `python car_insurance_premium_parser.py` on original/fixed versions respectively with these inputs in order:
1. `ka 01 ab 1234`
2. `12000;;800`
3. `14/08/1999`
The original exits before asking for DOB. The fixed program returns None for the malformed claims and continues, reporting age 27.

SS2 is the original failing fuzz run. SS4 uses `python -m pytest test_car_insurance_premium_parser.py test_regressions.py -q` on the fixed module. Text logs and full-page screenshots are in `evidence/`. Screenshots capture a browser displaying verbatim execution logs, not native terminal windows. The PDF includes all four captures, bug analysis and three reflections. The supplied handout has no explicit reflection questions, so these address findings, fixes and limitations requested by the repository README.

## Validation contract
- Non-string registration returns an empty string. Valid strings are uppercased and stripped of whitespace, dashes and dots. This is normalization, not jurisdiction-specific plate validation.
- Claims accepts semicolon-separated nonnegative ASCII whole numbers (1-100 digits each), allowing surrounding whitespace. Invalid input returns None; no tokens are silently discarded.
- DOB requires DD/MM/YYYY and a valid calendar date. Future years and invalid current_year return None. Age preserves the original calendar-year subtraction contract, not exact birthday age.
- Fuzz sampling and these regression tests do not establish correctness for all possible inputs or immunity to resource exhaustion.
