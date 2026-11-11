# Lab 6 - Code and Branch Coverage
Shreyas K M | PES1UG24AM402

Source: https://github.com/SETAPESU26/L6_L7_55_car_insurance_premium (snapshot 0ef1e60ba3890bc9b75430ab07010cd1a3a151f5). Application code is unchanged.

## Reproduce
From this folder, install `python -m pip install -r requirements.txt`, then run:

```sh
python -m coverage run --source=car_insurance_premium -m pytest CodeCoverageTest_car_insurance_premium.py
python -m coverage report -m
python -m coverage run --branch --source=car_insurance_premium -m pytest BranchCoverageTest_car_insurance_premium.py
python -m coverage report -m
```

## Results and analysis
The two starter tests passed but covered only 18/39 statements (46% line coverage). The initial combined statement/branch report was 41%. Baseline text logs are retained; only final results have screenshots.

The code coverage suite passes 24 tests and executes 39/39 statements (100%). The branch suite passes 27 tests and executes all 30/30 measured branch exits, with zero partial branches (100%). The branch report's Cover column combines statements and branch exits; the JSON report records branch totals separately.

Tests cover unknown car type, minimum driver age, ages 24/25 and 59/60, zero/one/two/three claims, anti-theft choices, bonus thresholds 0/1/3/5 and invalid negative years, total loss, damage equal to/below deductible, normal payout and insured-value caps. Both operands of the invalid-amount condition are exercised. Extra branch tests combine age surcharge, claim multiplier/discount and anti-theft deduction.

Line coverage measures executed statements; branch coverage measures decision exits. Neither proves all path combinations or all input contracts correct. Tests preserve the supplied behavior, including its limited validation.

`evidence/` includes raw logs, JSON metrics and screenshots of verbatim logs displayed in a browser evidence viewer. These are browser captures of real terminal output, not native terminal screenshots. Code and branch deliverables are recorded in separate commits.
