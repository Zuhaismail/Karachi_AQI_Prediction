import pandas as pd
import os

FORECAST_FILE = "forecast_next3days_all_models.csv"   # generated daily by forecast.py
HISTORY_FILE = "forecast_history.csv"                # forecast file

def update_forecast_history():
    if not os.path.exists(FORECAST_FILE):
        print(" No forecast file found. Run forecast.py first.")
        return

    # Load today's forecast
    new_forecast = pd.read_csv(FORECAST_FILE, parse_dates=["timestamp"])
    # Drop timezone if exists (force naive)
    new_forecast["timestamp"] = new_forecast["timestamp"].dt.tz_localize(None)
    new_forecast["forecast_run_date"] = pd.Timestamp.today().normalize().tz_localize(None)

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE, parse_dates=["timestamp", "forecast_run_date"])
        history["timestamp"] = history["timestamp"].dt.tz_localize(None)
        history["forecast_run_date"] = history["forecast_run_date"].dt.tz_localize(None)
        combined = pd.concat([history, new_forecast], ignore_index=True)
    else:
        combined = new_forecast

    # Rule: for each forecasted day, keep the run that is closest to that day
    combined["days_ahead"] = (combined["timestamp"].dt.normalize() - combined["forecast_run_date"]).dt.days.abs()

    # Sort so that for each timestamp, the smallest days_ahead (closest run) is first
    combined = combined.sort_values(["timestamp", "days_ahead", "forecast_run_date"])

    # Keep best forecast per date (drop duplicates, keeping the first after sorting)
    best_forecast = combined.drop_duplicates(subset=["timestamp"], keep="first")

    # Drop helper column
    best_forecast = best_forecast.drop(columns=["days_ahead"])

    # Save
    best_forecast.to_csv(HISTORY_FILE, index=False)

    print(f"Forecast history updated. Rows = {len(best_forecast)}")
    print(f"Saved to {HISTORY_FILE}")


if __name__ == "__main__":
    update_forecast_history()

