# Reflection

> The handout PDF doesn't list the four questions. These are the usual ones for this lab. Check them against your instructor's wording and rename the headings if needed.

**1. Which issues were the easiest and hardest to fix, and why?**
The easiest were the style issues (naming, unused imports, `== None`, blank lines) because the tool says exactly what to change. The hardest was `eval` in `compute_bonus`: removing it changed the function's interface (a formula string became a numeric `rate`), so the caller had to change too. Salting the PIN hash was also harder than swapping algorithms, because the output format changed.

**2. Did the tools report any false positives, or miss anything?**
Mostly accurate. Bandit's B105 on the token was a "Low/Medium confidence" guess based on the variable name, but here it was a real problem. The tools missed some things I found by running the program: the `service_fee` is never applied, and deposits/withdrawals accept negative amounts. Pylint and Flake8 flagged `service_fee` only as an *unused variable*, not as a missing business rule. Static analysis can't know what the code was meant to do.

**3. How would you integrate these tools into a real workflow?**
Run Flake8 and Pylint as a pre-commit hook so style problems never reach the repo. Run all three tools in CI (for example GitHub Actions) on every pull request and fail the build on Bandit High/Medium findings or a Pylint score below a threshold (such as 9.5).

**4. What were the tangible improvements in code quality, security and readability?**
Pylint went from 5.83 to 10.00, Bandit from 6 findings (2 High) to 0, and Flake8 from 15 warnings to 0. The code no longer allows command injection or arbitrary code execution, stores PINs with a salted slow hash, and no longer hides errors. It also has docstrings and consistent naming, and no longer runs on import, so it is easier to read and test.
