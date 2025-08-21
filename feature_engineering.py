import pandas as pd

# Load your AQI dataset
df = pd.read_csv("karachi_air_quality.csv", parse_dates=["timestamp"])

# Sort by time to ensure correct lag & rolling
df.sort_values("timestamp", inplace=True)
df.reset_index(drop=True, inplace=True)

# 1. Time-based Features

df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['weekday'] = df['timestamp'].dt.weekday
df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)


# Lag Features

df['lag_1'] = df['aqi'].shift(1)
df['lag_2'] = df['aqi'].shift(2)
df['lag_24'] = df['aqi'].shift(24)

# Rolling Statistics

df['rolling_mean_6h'] = df['aqi'].rolling(window=6).mean()
df['rolling_std_12h'] = df['aqi'].rolling(window=12).std()

# AQI Change Rate

df['aqi_diff'] = df['aqi'] - df['lag_1']
df['aqi_pct_change'] = df['aqi'].pct_change() * 100

# Pollutant Ratios

df['pm_ratio'] = df['pm2_5'] / df['pm10']
df['gas_ratio'] = (df['no2'] + df['so2'] + df['o3']) / df['co']

# Save Feature-Enhanced Dataset

df.to_csv("karachi_aqi_features.csv", index=False)
print("Feature engineering complete. Saved to: karachi_aqi_features.csv")

