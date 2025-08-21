import pandas as pd
import numpy as np
import joblib
from datetime import timedelta

# Models
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

# Load preprocessed data

scaler = joblib.load("scaler.pkl")
X_train, X_test, y_train, y_test = joblib.load("train_test.pkl")

#  Recover feature names
df_features = pd.read_csv("karachi_aqi_features.csv", parse_dates=["timestamp"])
feature_names = df_features.drop(columns=["timestamp", "aqi"]).columns
X_train = pd.DataFrame(X_train, columns=feature_names, index=y_train.index)
X_test = pd.DataFrame(X_test, columns=feature_names, index=y_test.index)

# Define Models 

models = {
    "RandomForest": RandomForestRegressor(
        n_estimators=200, random_state=42, n_jobs=-1
    ),
    "GradientBoosting": GradientBoostingRegressor(
        n_estimators=200, learning_rate=0.1, random_state=42
    ),
    "LightGBM": LGBMRegressor(
        n_estimators=200, learning_rate=0.05, random_state=42, n_jobs=-1
    )
}

results = {}

# Train + Evaluate Models

for name, model in models.items():
    print(f"Training {name} ...")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    results[name] = {"RMSE": round(rmse, 2), "MAE": round(mae, 2), "R2": round(r2, 3)}
    joblib.dump(model, f"{name}_model.pkl")

# Save metrics
joblib.dump(results, "results.pkl")
pd.DataFrame(results).T.to_csv("model_results.csv")

print("\nModel Performance:")
for k, v in results.items():
    print(f"{k}: RMSE={v['RMSE']}, MAE={v['MAE']}, R2={v['R2']}")

# Forecast Today + Next 3 Days (combined for all models)

df = pd.read_csv("karachi_aqi_features.csv", parse_dates=["timestamp"])
df.sort_values("timestamp", inplace=True)

# Initialize combined forecast DataFrame with timestamps
last_time = df.iloc[-1]["timestamp"]
timestamps = [last_time + timedelta(hours=i) for i in range(73)]  # today + 72 hours
combined_forecast = pd.DataFrame({"timestamp": timestamps})

for name in models.keys():
    print(f"\nForecasting with {name} ...")
    model = joblib.load(f"{name}_model.pkl")

    last_row = df.iloc[-1].copy()
    preds = []

    # First prediction = "today"
    features = last_row.drop(labels=["timestamp", "aqi"]).to_frame().T
    X_input = scaler.transform(features)
    X_input = pd.DataFrame(X_input, columns=feature_names)
    today_pred = model.predict(X_input)[0]
    preds.append(today_pred)

    # Predict next 72 hours
    temp_row = last_row.copy()
    temp_time = last_time
    for step in range(72):
        features = temp_row.drop(labels=["timestamp", "aqi"]).to_frame().T
        X_input = scaler.transform(features)
        X_input = pd.DataFrame(X_input, columns=feature_names)

        y_pred = model.predict(X_input)[0]
        preds.append(y_pred)

        # Update features for next step
        temp_row["lag_1"] = y_pred
        temp_row["lag_2"] = temp_row["lag_1"]
        temp_row["lag_24"] = temp_row.get("lag_23", y_pred)
        temp_row["rolling_mean_6h"] = (
            (temp_row["rolling_mean_6h"] * 5 + y_pred) / 6
        )
        temp_row["aqi_diff"] = y_pred - temp_row["lag_1"]
        temp_row["aqi_pct_change"] = (
            (temp_row["aqi_diff"] / temp_row["lag_1"]) * 100
            if temp_row["lag_1"] != 0
            else 0
        )
        temp_time += timedelta(hours=1)

    # Round predictions to 2 decimals
    combined_forecast[name] = np.round(preds, 2)

# Save one CSV with all models
combined_forecast.to_csv("forecast_next3days_all_models.csv", index=False)
print("\n Combined forecast saved to forecast_next3days_all_models.csv (values rounded to 2 decimals)")



