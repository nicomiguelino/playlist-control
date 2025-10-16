# Playing with Python Event Loops :fire:

A Python project exploring event loops and asynchronous programming.

## Setup

### Initialize Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Linting & Formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

### Check code

```bash
# Lint code
ruff check .

# Format code (check only)
ruff format --check .
```

### Auto-fix issues

```bash
# Fix linting issues
ruff check --fix .

# Format code
ruff format .
```
