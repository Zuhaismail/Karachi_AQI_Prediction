import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config

st.set_page_config(page_title=" Karachi AQI Predictor", layout="wide")

st.title(" Karachi AQI Prediction Dashboard")
st.write("Historical AQI data and 3-day forecast using LightGBM (selected as the best model).")

# Load Data

@st.cache_data
def load_data():
    history = pd.read_csv("karachi_air_quality.csv", parse_dates=["timestamp"])
    forecast = pd.read_csv("forecast_next3days_all_models.csv", parse_dates=["timestamp"])
    results = pd.read_csv("model_results.csv", index_col=0)
    return history, forecast, results

history, forecast, results = load_data()

# Show Historical AQI

st.subheader(" Historical AQI")
st.line_chart(history.set_index("timestamp")["aqi"])

latest_aqi = history.iloc[-1]["aqi"]
st.metric("Current AQI", f"{latest_aqi:.2f}")

# Show Model Performance

st.subheader(" Model Performance (Evaluation Metrics)")

def highlight_best(val, col):
    if col in ["RMSE", "MAE"]:
        return "background-color: lightgreen" if val == results[col].min() else ""
    elif col == "R2":
        return "background-color: lightgreen" if val == results[col].max() else ""
    return ""

styled = results.style.apply(
    lambda row: [highlight_best(v, col) for v, col in zip(row, results.columns)],
    axis=1
)

st.dataframe(styled)

# Forecast with LightGBM

best_model = "LightGBM"
st.success(f" Using **{best_model}** model for forecasting (based on evaluation results).")

st.subheader(f" 3-Day Forecast using {best_model}")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(history["timestamp"].iloc[-200:], history["aqi"].iloc[-200:], label="History", color="blue")
ax.plot(forecast["timestamp"], forecast[best_model], label=f"{best_model} Forecast", color="red")
ax.axhline(200, color="orange", linestyle="--", label="Unhealthy (200)")
ax.set_ylabel("AQI")
ax.set_xlabel("Time")
ax.legend()
st.pyplot(fig)

# Alerts

st.subheader(" Alerts")
if forecast[best_model].max() > 200:
    st.error(" Warning: Forecast indicates hazardous AQI (>200) in the next 3 days!")
else:
    st.success(" AQI is expected to remain below hazardous levels in the next 3 days.")

# Show Forecast Data Table

st.subheader(" Forecast Data")
st.dataframe(forecast[["timestamp", best_model]].rename(columns={best_model: "Forecasted AQI"}))

