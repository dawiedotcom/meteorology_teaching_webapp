# Metrology Teaching WebApp

Web front end for [Metrology_teaching](https://github.com/SimonTett/Meteorology_teaching)

## Setup with `uv`
```bash
uv venv
. .venv/bin/activate
uv pip install -r requirements.txt
```

## Setup with `virtualenv`

```bash
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
. .venv/bin/activate
./run_gunicorn.sh
```

## Update requirements.txt

Add dependancies in [pyproject.toml](pyproject.toml), then run:
```bash
uv pip compile pyproject.toml -o requirements.txt
```
