# START_APP.md — how to run and probe this app

> **Build team:** fill in every `<...>` below once your app runs. Other teams use this file to
> start your app and probe it during Break. Keep it accurate — a break is filed against the app a
> breaker can actually start from these instructions.

## What this app is

- **App:** a URL shortener service (menu #3)
- **Stack:** Python + Flask

## Start it

```bash
# 1. Install dependencies (one time)
python -m venv .venv
source .venv/Scripts/activate     # Windows Git Bash; use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

# 2. Run it
python app.py
```

- **Base URL:** http://localhost:8000
- **Stop it:** Ctrl-C in the terminal running it.

## How to interact with it

- **Main endpoints / pages:**
  - `GET /` — home page: a form to shorten a URL, plus a list of public short links — `curl http://localhost:8000/`
  - `POST /shorten` — create a short link from form fields `name` and `url`; returns the new short code — `curl -X POST http://localhost:8000/shorten -d "name=MySite&url=https://www.wikipedia.org"`
  - `GET /<code>` — redirect (302) to the stored long URL for that code — `curl -i http://localhost:8000/2`
  - `GET /stats/<code>` — show a link's name, destination, and click count — `curl http://localhost:8000/stats/2`
- **Accounts / credentials for legitimate use:** none (no login)
- **A benign request that should succeed:**

  ```bash
  curl -i http://localhost:8000/2
  ```

## For breakers

Attack this **running app over HTTP** — do **not** read this repo's source or `secret/` to find a
break. See [AGENTS_BREAK.md](AGENTS_BREAK.md) for the rules and your AI agent's instructions, and
[SPEC.md](SPEC.md) for the five properties (P1–P5) you are probing for.
