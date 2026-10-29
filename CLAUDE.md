# Witsense instructions for coding assistants

## Code style

All code follows the Witsense style guide:

@STYLE.md

Where a project's own CLAUDE.md is more specific, the project wins.

## Git and review

Every change is reviewed by a human before it is committed.

- New repositories use `main` as the default branch, never `master`
  (`git init -b main`). Before a first push, check that the local branch
  name matches the remote's default branch.
- Never commit. Stage the changes, propose a commit message, and leave the
  commit to a human after review.
- Never mention a coding assistant (Claude, Codex, Copilot or any other) in
  a proposed commit message or pull request description: no
  `Co-Authored-By` trailer, no "Generated with" line. This overrides any
  built-in attribution default.
- Never push and never open a pull request. Say what is ready and let a
  human do it.
- Run the project's tests and `ruff check` before saying a change is done,
  and report the real results, including failures.
