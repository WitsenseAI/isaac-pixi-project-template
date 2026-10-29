# Witsense code style

Code is read as the documentation. Comments and long functions are signs
that the names and the structure are not doing their job, so make the
structure carry the meaning.

`ruff.toml` checks the rules marked (checked). Reviewers check the rest.

## Names over comments

- Choose names that make a comment unnecessary.
- Minimum or zero comments. A comment is justified only when it explains a
  non-obvious *why*: a hardware constraint, a workaround for a library bug,
  a deliberate tradeoff. Never write a comment that restates *what* the code
  does.
- An unverified value or assumption counts as a non-obvious why. Say so in a
  comment next to it.
- PEP 8 naming. (checked)

## Small functions

- No function longer than about 15 lines. (checked, approximately, as a
  statement and branch count)
- When a function grows past that, extract named helpers. Do not split it
  into sections with comments.

## Idiomatic Python

- Type hints on public signatures. (checked)
- Comprehensions and stdlib idioms over manual loops. (partly checked)
- Early returns over nesting. (partly checked)

## No dead or speculative code

- No commented-out code, unused imports, variables, or arguments. (checked)
- No "for later" hooks, flags, or abstractions. Add them when they are needed.

## Docstrings

- Each script (anything under `scripts/` or `tools/`) keeps a module
  docstring: one line saying what it does, then the command that launches
  it (`pixi run <task>`, or the project's equivalent if it does not use
  pixi). (presence checked)
- No function or class docstrings. Ruff cannot flag a docstring that is
  present, so this one is on the reviewer.

```python
"""Train a navigation policy on prepared rover sessions.

pixi run train --config configs/smoke.yaml
"""
```
