import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
SESSION = requests.Session()

# ink / surface tokens (dark palette)
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
GRIDLINE = "#2c2c2a"
SURFACE_2 = "#1a1a19"
BORDER = "rgba(255,255,255,0.10)"
HIGH_COLOR = "#3987e5"   # categorical slot 1 (blue)
LOW_COLOR = "#d95926"    # categorical slot 2 (orange)

WEATHER_CODES = {
    0: ("Clear sky", "☀️", "clear"),
    1: ("Mainly clear", "🌤️", "clear"),
    2: ("Partly cloudy", "⛅", "cloudy"),
    3: ("Overcast", "☁️", "overcast"),
    45: ("Fog", "🌫️", "fog"),
    48: ("Depositing rime fog", "🌫️", "fog"),
    51: ("Light drizzle", "🌦️", "rain"),
    53: ("Moderate drizzle", "🌦️", "rain"),
    55: ("Dense drizzle", "🌦️", "rain"),
    56: ("Light freezing drizzle", "🌧️", "rain"),
    57: ("Dense freezing drizzle", "🌧️", "rain"),
    61: ("Slight rain", "🌧️", "rain"),
    63: ("Moderate rain", "🌧️", "rain"),
    65: ("Heavy rain", "🌧️", "rain"),
    66: ("Light freezing rain", "🌧️", "rain"),
    67: ("Heavy freezing rain", "🌧️", "rain"),
    71: ("Slight snow fall", "🌨️", "snow"),
    73: ("Moderate snow fall", "🌨️", "snow"),
    75: ("Heavy snow fall", "❄️", "snow"),
    77: ("Snow grains", "❄️", "snow"),
    80: ("Slight rain showers", "🌦️", "rain"),
    81: ("Moderate rain showers", "🌦️", "rain"),
    82: ("Violent rain showers", "⛈️", "storm"),
    85: ("Slight snow showers", "🌨️", "snow"),
    86: ("Heavy snow showers", "🌨️", "snow"),
    95: ("Thunderstorm", "⛈️", "storm"),
    96: ("Thunderstorm with slight hail", "⛈️", "storm"),
    99: ("Thunderstorm with heavy hail", "⛈️", "storm"),
}

GROUP_GRADIENTS = {
    "clear": "linear-gradient(135deg, #c98500 0%, #d95926 100%)",
    "cloudy": "linear-gradient(135deg, #3987e5 0%, #52514e 100%)",
    "overcast": "linear-gradient(135deg, #52514e 0%, #2c2c2a 100%)",
    "fog": "linear-gradient(135deg, #6b6b68 0%, #383835 100%)",
    "rain": "linear-gradient(135deg, #184f95 0%, #3987e5 100%)",
    "snow": "linear-gradient(135deg, #184f95 0%, #6da7ec 100%)",
    "storm": "linear-gradient(135deg, #0d0d0d 0%, #4a3aa7 100%)",
}

UNIT_PARAMS = {
    "°C": {"temperature_unit": "celsius", "wind_speed_unit": "kmh", "wind_label": "km/h"},
    "°F": {"temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "wind_label": "mph"},
}


def describe(code: int) -> tuple[str, str, str]:
    return WEATHER_CODES.get(code, ("Unknown", "❓", "cloudy"))


def html(s: str) -> str:
    """Collapse an indented multi-line HTML literal to one line.

    Markdown treats any line indented 4+ spaces as a code block, and Python's
    indentation puts exactly that much leading whitespace on template strings
    built inside nested blocks — so raw HTML tags leak into the page as text
    unless the indentation is stripped before st.markdown renders it.
    """
    return "".join(line.strip() for line in s.strip().splitlines())


@st.cache_data(ttl=600)
def geocode(city: str):
    resp = SESSION.get(GEOCODE_URL, params={"name": city, "count": 5, "language": "en"}, timeout=10)
    resp.raise_for_status()
    return resp.json().get("results") or []


@st.cache_data(ttl=600)
def get_weather(lat: float, lon: float, unit: str):
    u = UNIT_PARAMS[unit]
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m",
                     "wind_speed_10m", "weather_code", "precipitation"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "temperature_unit": u["temperature_unit"],
        "wind_speed_unit": u["wind_speed_unit"],
        "timezone": "auto",
        "forecast_days": 7,
    }
    resp = SESSION.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=600)
def forecast_chart(daily: dict, unit: str) -> go.Figure:
    days = pd.to_datetime(daily["time"]).strftime("%a")
    highs = daily["temperature_2m_max"]
    lows = daily["temperature_2m_min"]

    def end_labels(vals):
        return [f"{v:g}°" if i == len(vals) - 1 else "" for i, v in enumerate(vals)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(days), y=lows, name=f"Low ({unit})", mode="lines+markers+text",
        line=dict(color=LOW_COLOR, width=2, shape="spline", smoothing=0.3),
        marker=dict(size=8, color=LOW_COLOR, line=dict(width=2, color=SURFACE_2)),
        text=end_labels(lows), textposition="bottom center",
        textfont=dict(color=INK_SECONDARY, size=13),
    ))
    fig.add_trace(go.Scatter(
        x=list(days), y=highs, name=f"High ({unit})", mode="lines+markers+text",
        line=dict(color=HIGH_COLOR, width=2, shape="spline", smoothing=0.3),
        marker=dict(size=8, color=HIGH_COLOR, line=dict(width=2, color=SURFACE_2)),
        fill="tonexty", fillcolor="rgba(57,135,229,0.12)",
        text=end_labels(highs), textposition="top center",
        textfont=dict(color=INK_PRIMARY, size=13),
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color=INK_SECONDARY),
        margin=dict(l=8, r=8, t=48, b=8),
        height=280,
        hovermode="x unified",
        hoverlabel=dict(bgcolor=SURFACE_2, bordercolor=BORDER, font=dict(color=INK_PRIMARY)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                     bgcolor="rgba(0,0,0,0)", font=dict(color=INK_SECONDARY)),
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(color=INK_MUTED)),
        yaxis=dict(showgrid=True, gridcolor=GRIDLINE, gridwidth=1, zeroline=False,
                    tickfont=dict(color=INK_MUTED), ticksuffix="°"),
    )
    return fig


st.set_page_config(page_title="Weather", page_icon="⛅", layout="centered")

st.markdown(f"""
<style>
:root {{
    --ink-primary: {INK_PRIMARY};
    --ink-secondary: {INK_SECONDARY};
    --ink-muted: {INK_MUTED};
    --surface-2: {SURFACE_2};
    --border: {BORDER};
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 760px; }

.app-title { font-size: 1.6rem; font-weight: 700; color: var(--ink-primary); margin-bottom: 0.25rem; }
.app-subtitle { color: var(--ink-muted); font-size: 0.95rem; margin-bottom: 1.25rem; }

.hero-card {
    border-radius: 20px; padding: 28px 28px; margin: 4px 0 20px 0;
    border: 1px solid var(--border);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.hero-top { display: flex; justify-content: space-between; align-items: flex-start; }
.hero-place { font-size: 1.15rem; font-weight: 600; color: var(--ink-primary); }
.hero-updated { font-size: 0.78rem; color: rgba(255,255,255,0.75); margin-top: 2px; }
.hero-icon { font-size: 52px; line-height: 1; }
.hero-temp { font-size: 4.2rem; font-weight: 700; color: var(--ink-primary); line-height: 1; margin-top: 6px; }
.hero-desc { font-size: 1.05rem; color: rgba(255,255,255,0.92); margin-top: 4px; }
.hero-range { font-size: 0.9rem; color: rgba(255,255,255,0.75); margin-top: 10px; }

.tile-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 22px; }
.tile {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 14px;
    padding: 14px 12px;
}
.tile-icon { font-size: 20px; margin-bottom: 6px; }
.tile-label { font-size: 0.75rem; color: var(--ink-muted); }
.tile-value { font-size: 1.35rem; font-weight: 600; color: var(--ink-primary); margin-top: 2px; }

.section-title { font-size: 1.05rem; font-weight: 600; color: var(--ink-primary); margin: 6px 0 8px 0; }

.day-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; margin-top: 4px; }
.day-card {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 12px;
    padding: 10px 4px; text-align: center;
}
.day-name { font-size: 0.78rem; color: var(--ink-secondary); font-weight: 600; }
.day-icon { font-size: 22px; margin: 4px 0; }
.day-high { font-size: 0.85rem; color: var(--ink-primary); font-weight: 600; }
.day-low { font-size: 0.78rem; color: var(--ink-muted); }

@media (max-width: 640px) {
    .tile-grid { grid-template-columns: repeat(2, 1fr); }
    .day-grid { grid-template-columns: repeat(4, 1fr); gap: 8px 8px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">⛅ Weather</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Search any city for current conditions and a 7-day outlook.</div>',
            unsafe_allow_html=True)

top_l, top_r = st.columns([3, 1])
with top_l:
    city = st.text_input("City", placeholder="Search a city, e.g. London, Tokyo, New York",
                          label_visibility="collapsed")
with top_r:
    unit = st.radio("Unit", ["°C", "°F"], horizontal=True, label_visibility="collapsed")

if city:
    try:
        results = geocode(city)
    except requests.RequestException as e:
        st.error(f"Could not reach the weather service: {e}")
        results = []

    if not results:
        st.warning("No matching city found. Try a different name.")
    else:
        options = {
            ", ".join(filter(None, [r["name"], r.get("admin1"), r["country"]])): r
            for r in results
        }
        choice = st.selectbox("Select location", list(options.keys()), label_visibility="collapsed")
        place = options[choice]

        try:
            data = get_weather(place["latitude"], place["longitude"], unit)
        except requests.RequestException as e:
            st.error(f"Could not fetch weather data: {e}")
            st.stop()

        current = data["current"]
        daily = data["daily"]
        desc, icon, group = describe(current["weather_code"])
        gradient = GROUP_GRADIENTS.get(group, GROUP_GRADIENTS["cloudy"])
        wind_unit = UNIT_PARAMS[unit]["wind_label"]
        updated = pd.to_datetime(current["time"]).strftime("%a %I:%M %p").lstrip("0")

        st.markdown(html(f"""
        <div class="hero-card" style="background:{gradient};">
            <div class="hero-top">
                <div>
                    <div class="hero-place">{place['name']}</div>
                    <div class="hero-updated">Updated {updated}</div>
                </div>
                <div class="hero-icon">{icon}</div>
            </div>
            <div class="hero-temp">{current['temperature_2m']:g}{unit}</div>
            <div class="hero-desc">{desc}</div>
            <div class="hero-range">H:{daily['temperature_2m_max'][0]:g}° &nbsp;L:{daily['temperature_2m_min'][0]:g}°</div>
        </div>
        """), unsafe_allow_html=True)

        tiles = [
            ("🌡️", "Feels like", f"{current['apparent_temperature']:g}{unit}"),
            ("💧", "Humidity", f"{current['relative_humidity_2m']}%"),
            ("🌬️", "Wind", f"{current['wind_speed_10m']:g}<span style=\"font-size:0.9rem;\"> {wind_unit}</span>"),
            ("☔", "Precipitation", f"{current['precipitation']:g}<span style=\"font-size:0.9rem;\"> mm</span>"),
        ]
        tile_cards = [html(f"""
            <div class="tile">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-value">{value}</div>
            </div>
            """) for icon, label, value in tiles]
        st.markdown(f'<div class="tile-grid">{"".join(tile_cards)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">7-Day Trend</div>', unsafe_allow_html=True)
        st.plotly_chart(forecast_chart(daily, unit), width="stretch",
                         config={"displayModeBar": False})

        st.markdown('<div class="section-title">Daily Forecast</div>', unsafe_allow_html=True)
        day_labels = pd.to_datetime(daily["time"]).strftime("%a")
        cards = []
        for i in range(len(daily["time"])):
            d_desc, d_icon, _ = describe(daily["weather_code"][i])
            day_name = "Today" if i == 0 else day_labels[i]
            cards.append(html(f"""
            <div class="day-card" title="{d_desc}">
                <div class="day-name">{day_name}</div>
                <div class="day-icon">{d_icon}</div>
                <div class="day-high">{daily['temperature_2m_max'][i]:g}°</div>
                <div class="day-low">{daily['temperature_2m_min'][i]:g}°</div>
            </div>
            """))
        st.markdown(f'<div class="day-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
else:
    st.info("Enter a city name above to see the current weather and forecast.")
