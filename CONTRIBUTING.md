# Contributing to Information Retrieval System

Thank you for your interest in improving this project.

## Development setup

```bash
git clone https://github.com/mazyar-ghezelji/information-retrieval-system.git
cd information-retrieval-system
pip install -e ".[dev,notebook]"
```

## Running tests

```bash
pytest
pytest -v --cov=ir
```

## Code style

- Use type hints for function signatures where helpful.
- Prefer `pathlib.Path` over string paths.
- Use `with open(...)` for all file I/O.

## Pull requests

1. Open an issue or comment on an existing one to discuss the change.
2. Fork the repo, create a branch, and make your changes.
3. Ensure tests pass and add tests for new behavior.
4. Submit a pull request with a clear description.

## Reporting issues

Include your Python version, how you installed the package, and the full error message or steps to reproduce.
