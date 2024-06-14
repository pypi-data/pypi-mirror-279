# runloop-py
The Runloop python SDK

## setup

### python

1. Install Python 3.12

```brew install python@3.12```

2. We use `uv` for python dependency management.  Instal `uv` via brew

```brew install uv```

3. Create a Python virtual environment using `uv` and source dependencies

```uv venv -p python3.12 && source .venv/bin/activate```

4. Install requirements

For `wrapper.main`:

```uv pip install -r requirements.txt```

For `wrapper.tests`:

```uv pip install -r requirements.txt && uv pip install -r requirements-test.txt```

### Linting
We use `ruff` to perform lint and formatting. To validate before submitting a PR, install ruff
```commandline
brew install ruff
```
Check your code.  Ruff will attempt to fix simple violations
```commandline
ruff check . --fix
```

