import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# LightGBM
from lightgbm import LGBMRegressor

# Load preprocessed data
scaler = joblib.load("scaler.pkl")
X_train, X_test, y_train, y_test = joblib.load("train_test.pkl")

# Load feature dataset 
df_features = pd.read_csv("karachi_aqi_features.csv")
feature_cols = [c for c in df_features.columns if c not in ["timestamp", "aqi"]]

X_train = pd.DataFrame(X_train, columns=feature_cols)
X_test = pd.DataFrame(X_test, columns=feature_cols)

# Models

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

# Train, Evaluate, Save
results = {}

for name, model in models.items():
    print(f" Training {name} ...")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    results[name] = {"Models": name, "RMSE": rmse, "MAE": mae, "R2": r2}

    # Save trained model
    joblib.dump(model, f"{name}_model.pkl")

# Save results

joblib.dump(results, "results.pkl")

print("\nTraining complete. Model performance:")
for k, v in results.items():
    print(f"{k}: RMSE={v['RMSE']:.2f}, MAE={v['MAE']:.2f}, R2={v['R2']:.3f}")

# Save CSV with "Model"
pd.DataFrame(results.values()).to_csv("model_results.csv", index=False)

