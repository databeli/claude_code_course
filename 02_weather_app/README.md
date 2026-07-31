# ⛅ Weather

A single-file Streamlit app: search a city, get current conditions and a 7-day forecast (chart + daily cards) in a dark UI. Powered by the free [Open-Meteo](https://open-meteo.com/) geocoding and forecast APIs — no API key needed. Responses cache for 10 minutes.

## Setup & Run

Windows (venv already present):

```
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\pip.exe install -r requirements.txt --quiet
.\venv\Scripts\python.exe -m streamlit run app.py --server.headless true --server.port 8501
```

macOS/Linux or fresh environment:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501. Requires Python 3.9+; deps in [requirements.txt](requirements.txt).

## Structure

Everything lives in `app.py` — no backend, database, build step, or tests. `.streamlit/config.toml` holds the theme. See [AGENTS.md](AGENTS.md) for architecture notes when extending it (e.g. adding weather codes).
