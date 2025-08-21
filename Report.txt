# Karachi AQI Prediction — End‑to‑End Report

**Student:** Zuha M. Ismail
**Location:** Karachi, Pakistan
**Dates covered:** 1 June 2025 → present (hourly)

---

## 1) Executive Summary

This project builds an **AQI (Air Quality Index) prediction system for Karachi**. Data are collected every hour from the OpenWeather API, converted into a **continuous EPA-style AQI value**, enriched with useful features, cleaned, and then used to train three machine learning models — **Random Forest, Gradient Boosting, and LightGBM**. The **best model (LightGBM)** is used to forecast AQI for the **next 3 days**. The results are shown in a **Streamlit dashboard** that updates automatically every day via GitHub Actions.

---

## 2) Problem & Objectives

**Problem:** Karachi often faces bad air quality. Just knowing categories (Good, Moderate, Poor) is not enough for people to plan.

**Objective:** Build a pipeline that:

1. Collects **hourly pollutant data**.
2. Converts it into **continuous AQI**.
3. Creates extra features from the data.
4. Trains models to predict AQI.
5. Forecasts AQI for the **next 72 hours**.
6. Shows results in a dashboard that **refreshes daily**.

---

## 3) Data Source & Collection

* **Source:** OpenWeather Air Pollution API.
* **Location:** Karachi (24.8607, 67.0011).
* **Period:** From **01‑Jun‑2025** to present, hourly.
* **Stored file:** `karachi_air_quality.csv`.

**Columns explained:**

* **timestamp** → date and time (hourly).
* **aqi** → Air Quality Index value (continuous after conversion).
* **co** → Carbon Monoxide.
* **no** → Nitric Oxide.
* **no2** → Nitrogen Dioxide.
* **o3** → Ozone.
* **so2** → Sulphur Dioxide.
* **pm2\_5** → Fine particles (2.5 microns).
* **pm10** → Coarse particles (10 microns).
* **nh3** → Ammonia.

---

## 4) Why use the EPA Formula?

OpenWeather gives only a **level AQI (1–5)**. We need **continuous values (0–500)** for better analysis and model training.

**Short formula:**
$AQI = ( (I_hi – I_lo) / (C_hi – C_lo) ) × (C – C_lo) + I_lo$

This means we find where the pollutant concentration falls between two ranges and scale it to the AQI range. For Karachi, **PM2.5 and PM10** usually dominate, so their sub-indices are calculated and the **higher one is taken** as the AQI.

---

## 5) Feature Engineering

After the raw data, new features were added:

* **hour, day, month, weekday, is\_weekend** → capture time patterns.
* **lag\_1, lag\_2, lag\_24** → use previous values to learn trends.
* **rolling\_mean\_6h, rolling\_std\_12h** → short-term average and variation.
* **aqi\_diff, aqi\_pct\_change** → how AQI is changing.
* **pm\_ratio** → ratio of fine to coarse particles.
* **gas\_ratio** → relation of gases to CO.

Output file: `karachi_aqi_features.csv`.

---

## 6) Data Preprocessing

* Removed **missing/invalid values**.
* **Chronological split:** first 80% train, last 20% test (to avoid future data leakage).
* **Scaling:** features standardized with `StandardScaler`.
* Saved: `scaler.pkl`, `train_test.pkl`.

---

## 7) Models Used

Three machine learning models were trained and compared:

1. Random Forest Regressor

Works by building many decision trees on random samples of data and averaging their results.

Strong at handling noisy data and capturing non-linear relations.

Advantage: Stable results without much tuning.

Limitation: Can be slower with very large datasets and may not capture long-term trends as well as boosting.

2. Gradient Boosting Regressor

Builds trees one after another, each trying to correct the mistakes of the previous one.

Learns complex relationships and is good for time-series style tabular data.

Advantage: More accurate than Random Forest in many cases.

Limitation: Slower to train and sensitive to hyperparameters like learning rate.

3. LightGBM Regressor

A modern boosting algorithm designed for speed and efficiency.

Uses leaf-wise tree growth, which often gives better accuracy.

Works very well with engineered features such as lags and rolling stats.

Advantage: Fast training and high accuracy.

Limitation: Needs some care to avoid overfitting on small datasets.

---

## 8) Evaluation (RMSE, MAE, R²)

* **RMSE:** measures large errors (lower is better).
* **MAE:** average error (lower is better).
* **R²:** tells how well the model explains the data (closer to 1 means better). A higher R² means the model fits the data well.

**Result:** LightGBM gave the **lowest errors** and **highest R²**, so it was chosen as the **final model**.

---

## 9) Forecasting (Next 72 Hours)

* Predicts one hour ahead, then uses that prediction to forecast the next, continuing for 72 hours.
* Updates lag and rolling features step by step.
* Final output: `forecast_next3days_all_models.csv`.

---

## 10) Streamlit Dashboard

* **Historical AQI chart** and latest value.
* **Model performance table** with highlights for best results.
* **Forecast chart (LightGBM)** with alert line at AQI 200 (Unhealthy).
* **Forecast table** for inspection.

📌 **LightGBM is used in the app because it gave the best fit and accuracy.**

---

## 11) Automation with GitHub Actions

* Daily script runs automatically.
* At **12:00 PM Karachi time** (7:00 AM UTC), it fetches new data, retrains, forecasts, and updates the app.

---

## 12) Results & Interpretation

* **AQI forecast is refreshed daily**.
* Dashboard alerts if AQI is expected to go above **200 (Unhealthy)**.
* LightGBM proved most reliable because of higher R² and lower errors.

