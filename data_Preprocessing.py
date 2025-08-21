import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


# Load engineered dataset

df = pd.read_csv("karachi_aqi_features.csv", parse_dates=["timestamp"])

## Clean data

# Drop rows with NaNs (from lags/rolling stats)
df = df.dropna()

# Replace inf/-inf (from pollutant ratios etc.)
df = df.replace([np.inf, -np.inf], np.nan)

# Drop rows with NaNs again (after replacement)
df = df.dropna()

# Define Features & Target
X = df.drop(columns=["timestamp", "aqi"])
y = df["aqi"]

# Safety check: Ensure all finite values

if not np.isfinite(X.to_numpy()).all():
    raise ValueError(" Features still contain NaN or Inf after cleaning!")

# Train-Test Split (last 20% = test set for realistic forecasting)

split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

#  Scale Features

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save Artifacts

joblib.dump(scaler, "scaler.pkl")
joblib.dump((X_train_scaled, X_test_scaled, y_train, y_test), "train_test.pkl")

print("Data preprocessing complete. Cleaned, scaled, and saved.")
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

