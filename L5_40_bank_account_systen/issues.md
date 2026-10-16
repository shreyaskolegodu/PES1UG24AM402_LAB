# Issues Found – bank_account_system.py

Line numbers refer to the original file. Ordered by severity (High → Low).

| # | Issue | Type | Line(s) | Tool / ID | Description | Fix Approach |
|---|-------|------|---------|-----------|-------------|--------------|
| 1 | OS command injection | Security (High) | 47 | Bandit B605 | `os.system("echo ... " + filename)` runs through a shell with a caller-controlled string. | Removed the shell call and used `print()` instead. |
| 2 | Weak hash for PINs | Security (High) | 38 | Bandit B324 | MD5 is broken and unsalted, so a 4-digit PIN can be cracked instantly. | Replaced with salted PBKDF2-HMAC-SHA256 (`hashlib.pbkdf2_hmac`, 200k iterations). |
| 3 | Use of `eval` | Security (Medium) | 34 | Bandit B307, Pylint W0123 | `eval(expr)` executes arbitrary code passed as a string. | `compute_bonus` now takes a numeric `rate` and returns `balance * rate`. |
| 4 | Insecure random for PIN | Security (Low) | 41 | Bandit B311 | `random` is predictable and unsuitable for secrets. | Used `secrets.randbelow(9000) + 1000`. |
| 5 | Hard-coded secret | Security (Low) | 50, 58 | Bandit B105 | Admin token stored in source and printed to the console. | Read it from the `BANK_ADMIN_TOKEN` env variable and print only whether it is set. |
| 6 | Bare `except: pass` | Bug / Security (Low) | 19-20 | Bandit B110, Pylint W0702, Flake8 E722 | Hides all errors, so a deposit to a missing account silently does nothing. | Removed the try/except; `deposit` validates the account and amount and returns True/False. |
| 7 | Mutable default argument | Bug | 9 | Pylint W0102 | `transactions=[]` is shared across all calls. | Default is `None`; a new list is created inside the function. |
| 8 | Service fee never charged | Logic bug | 23 | Pylint W0612, Flake8 F841 | `service_fee = 2.50` is assigned but never used, so withdrawals are fee-free (output showed 1300). | Made it a `SERVICE_FEE` constant and deduct `amount + SERVICE_FEE` (balance now 1297.5). |
| 9 | Missing input validation | Bug | 16-30 | Manual review | Negative or zero amounts could be deposited or withdrawn. | Reject `amount <= 0` and unknown accounts. |
| 10 | File not closed safely | Quality | 44-46 | Pylint R1732, W1514 | Manual `open`/`close` leaks the handle on error; no encoding given. | Used `with open(..., encoding="utf-8")` and `json.dump` instead of `str(dict)`. |
| 11 | Bad function name | Style | 9 | Pylint C0103 | `createAccount` is not snake_case. | Renamed to `create_account`. |
| 12 | Comparison to None | Style | 24 | Pylint C0121, Flake8 E711 | `== None`. | Replaced with a membership check (`not in`), equivalent to `is None`. |
| 13 | Unnecessary else after return | Style | 28 | Pylint R1705 | `else` after `return`. | Removed the `else`. |
| 14 | Missing docstrings | Style | all functions | Pylint C0116 | No function documentation. | Added one-line docstrings. |
| 15 | Old `%` formatting | Style | 13 | Pylint C0209 | `%` string formatting. | Converted to an f-string. |
| 16 | Unused import `sys` / unused `random` | Style | 5 | Pylint W0611, Flake8 F401 | Dead imports. | Removed. |
| 17 | `main()` runs on import | Design | 60 | Manual review | Importing the module runs the demo. | Added `if __name__ == "__main__":` guard. |
| 18 | PEP 8 formatting | Style | 9, 16, 22, 32, 37, 40, 43, 49, 60, 13 | Flake8 E302, E305, E501 | Missing blank lines; line is 89 chars. | Two blank lines between top-level defs; wrapped long line. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.83 / 10 | 10.00 / 10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 15 warnings | 0 warnings |

## Commits
1. Fix Bandit findings
2. Fix Pylint findings
3. Fix Flake8 findings
