# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-file Streamlit weather app ([app.py](app.py)). User searches a city, picks a matching location from geocoding results, and sees current conditions plus a 7-day forecast (chart + daily cards). No backend, no database, no build step — everything lives in `app.py`.

## Commands

Windows venv paths (no activation needed, call the exe directly):

```
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\pip.exe install -r requirements.txt --quiet
.\venv\Scripts\python.exe -m streamlit run app.py --server.headless true --server.port 8501
```

There is no test suite, lint config, or build step in this repo.

## Architecture

`app.py` is organized top-to-bottom as: constants/palette → data fetch → chart builder → page render. All the state that matters lives in this ordering — there's no separate module boundary to preserve.

- **Data flow**: `geocode(city)` → `GEOCODE_URL` (Open-Meteo geocoding) returns candidate locations → user picks one via `st.selectbox` → `get_weather(lat, lon, unit)` → `FORECAST_URL` (Open-Meteo forecast) returns current + daily data. Both calls are wrapped in `@st.cache_data(ttl=600)`.
- **Weather code mapping**: `WEATHER_CODES` maps Open-Meteo's numeric weather codes to `(description, emoji, group)`. `group` (e.g. `"rain"`, `"storm"`, `"clear"`) feeds `GROUP_GRADIENTS` to pick the hero card's background gradient. When adding a new Open-Meteo weather code, update both dicts together.
- **HTML rendering quirk**: Streamlit's markdown renderer treats 4+ leading spaces as a code block, but Python indentation naturally produces that much whitespace on f-strings built inside `if`/`for` blocks. The `html()` helper strips per-line indentation before every `st.markdown(..., unsafe_allow_html=True)` call — always route generated HTML through `html()` rather than passing an indented multi-line f-string directly.
- **Styling**: all CSS is injected once via a single `st.markdown("""<style>...""", unsafe_allow_html=True)` block near the top of the render section. Color tokens are declared as module-level constants (`INK_PRIMARY`, `SURFACE_2`, etc.) and reused both in the CSS block and in Plotly figure styling (`forecast_chart`) so the dark theme stays consistent between native HTML tiles and the chart. `.streamlit/config.toml` sets the matching dark theme for Streamlit's own chrome.
- **Units**: `unit` (`"°C"`/`"°F"`) is threaded through both API requests (Open-Meteo wants `fahrenheit`/`celsius` and `mph`/`kmh`) and display strings — when changing unit handling, update both `get_weather`'s `params` and the f-strings that render values.

