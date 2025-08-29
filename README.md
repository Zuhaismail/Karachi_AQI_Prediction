# 🌍 Karachi AQI Prediction

## 📌 Project Overview  

This project builds an **AQI (Air Quality Index) prediction system for Karachi** that:  

- Collects **hourly air quality data** via the [OpenWeather API](https://openweathermap.org/api/air-pollution)  
- Converts raw data into **EPA AQI values (0–500)**  
- Performs **feature engineering & EDA**  
- Trains **3 machine learning models** (Random Forest, Gradient Boosting, LightGBM)  
- Forecasts **next 72 hours of AQI**  
- Deploys results to a **Streamlit dashboard** that **updates daily** via GitHub Actions  

🔗 **Live Dashboard:** [Karachi AQI Prediction](https://karachiaqiprediction-ene5lvsysk6fqdwbgnk75s.streamlit.app/)  

---

## 🎯 Problem & Objectives  

**Problem:** Karachi faces persistent poor air quality. Traditional AQI reports only show categories (Good, Moderate, Poor), which lack predictive insights.  

**Objectives:**  
✔ Collect hourly pollutant data  
✔ Compute continuous AQI values  
✔ Engineer predictive features  
✔ Train & evaluate ML models  
✔ Forecast **72-hour AQI**  
✔ Deploy an **auto-updating dashboard**  

---

## 🗂️ Data Pipeline  

📁 **Data Files:**  
- `karachi_air_quality.csv` → Raw data from API (hourly pollutants)  
- `karachi_aqi_features.csv` → After feature engineering  
- `model_results.csv` → ML model evaluation  
- `forecast_next3days_all_models.csv` → Forecasts (all models)  
- `forecast_history.csv` → Archived daily forecasts  

📜 **Scripts:**  
| Script | Purpose |
|--------|---------|
| `api_parser.py` | Fetch hourly data from OpenWeather API |
| `feature_engineering.py` | Create time, lag, rolling features |
| `EDA.ipynb` | Exploratory Data Analysis |
| `data_Preprocessing.py` | Scaling, splitting, cleaning |
| `train_models.py` | Train & evaluate RF, GBM, LightGBM |
| `forecast.py` | Predict next 72 hours |
| `forecastDataSaved.py` | Store forecast history |
| `app.py` | Streamlit dashboard |
| `.github/workflows/` | GitHub Actions automation |

---

## 📐 Why EPA AQI Formula?  

OpenWeather provides AQI **levels (1–5)**, but detailed forecasting requires **continuous values (0–500)**.  
EPA formula maps pollutant concentrations → AQI sub-indices.  

👉 For Karachi, **PM2.5 & PM10 dominate** → higher sub-index used as AQI.  

---

## 🔍 EDA Insights  

- **Shape:** `1,980 rows × 24 cols`  
- **Correlations with AQI:**  
  - Strong → PM2.5 (0.99), PM10 (0.97)  
  - Moderate → O3 (0.58), SO2 (0.50)  
  - Weak → NO, NO2, CO, NH3  
- **Categories:** Mostly *Moderate* & *Unhealthy for Sensitive Groups*  
- **Patterns:** Higher AQI in evenings & weekends  

✅ AQI in Karachi is **driven mainly by particulate matter**.  

---

## 🤖 Models  

| Model | Pros | Cons |
|-------|------|------|
| 🌲 Random Forest | Stable, noise-resistant | Slower, less accurate |
| 🔥 Gradient Boosting | Strong for tabular time-series | Slower training |
| ⚡ LightGBM | Fast, accurate, efficient | Risk of overfitting |

📊 **Evaluation Metrics:** RMSE, MAE, R²  
✅ **LightGBM performed best**  

---

## ⏳ Forecasting (Next 72 Hours)  

- Forecast horizon: **72h ahead**  
- Iterative predictions with lag & rolling features  
- Saved outputs:  
  - `forecast_next3days_all_models.csv`  
  - `forecast_history.csv`  

---

## 📊 Streamlit Dashboard  

Features:  
✔ Historical AQI trends  
✔ Current AQI  
✔ Model performance comparison  
✔ Forecast chart (LightGBM, alerts at AQI > 200)  
✔ Auto-updating every day  

🔗 [Streamlit Dashboard](https://karachiaqiprediction-ene5lvsysk6fqdwbgnk75s.streamlit.app/)  

---

## ⚙️ Automation (GitHub Actions)  

- Runs **daily @ 12:00 PM Karachi time**  
- Workflow:  
  1. Fetch new data  
  2. Preprocess & retrain models  
  3. Forecast next 72 hours  
  4. Update dashboard & push results  

---

## ✅ Results & Takeaways  

- Karachi’s air quality is **rarely “Good”**  
- Most hours fall into **Moderate** or **Unhealthy for Sensitive Groups**  
- **PM2.5 & PM10 = key drivers** of poor AQI  
- **LightGBM** is best for AQI forecasting  
- Fully automated → **zero manual updates**  

---

## 👩‍💻 Author  

**Zuha Muhammad Ismail**  
🔗 [GitHub Repo](https://github.com/Zuhaismail/Karachi_AQI_Prediction)  

---
