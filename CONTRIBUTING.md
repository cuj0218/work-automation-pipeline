# Contributing

Thanks for helping improve Work Automation Pipeline.

Good first contributions include:

- Add a new example task inventory for a real team workflow.
- Improve the generated report wording.
- Add validation for common CSV mistakes.
- Document a repeatable workplace automation case study.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m pip install pytest
python -m pytest
```

## Pull Request Checklist

- Keep changes focused on one workflow or one behavior.
- Add or update tests for code changes.
- Update README examples when user-facing behavior changes.
