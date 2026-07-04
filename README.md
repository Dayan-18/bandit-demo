# Bandit SAST Demo

Demo project for the article **"Finding Security Bugs Before They Ship: Applying Bandit (SAST) to a Python Web App"**.

- `app.py` — intentionally vulnerable Flask app (7 classic security issues)
- `app_fixed.py` — remediated version (0 Bandit findings)
- `.github/workflows/bandit.yml` — GitHub Actions workflow that runs Bandit on every push/PR

## Run locally

```bash
pip install -r requirements.txt
bandit app.py        # 10 findings
bandit app_fixed.py  # 0 findings
```

⚠️ `app.py` is intentionally insecure. Never deploy it.
