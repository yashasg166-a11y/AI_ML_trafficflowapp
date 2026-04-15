import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os

print("--- Bengaluru Traffic ML Model Training ---")

# 1. Load the original CSV
csv_path = r"archive (2)\Metro_Interstate_Traffic_Volume.csv"
print(f"Loading data from {csv_path}...")
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"ERROR: Could not find {csv_path}")
    exit(1)

# 2. Extract core features from the dataset
print("Extracting features from timestamp...")
df['date_time'] = pd.to_datetime(df['date_time'])
df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek # 0=Monday, 6=Sunday

# 3. Normalize Traffic Volume to a Percentage (0-100)
# Max volume in this typical dataset is ~7280
max_vol = df['traffic_volume'].max()
if max_vol == 0: max_vol = 7000
df['traffic_pct'] = (df['traffic_volume'] / max_vol) * 100
df['traffic_pct'] = df['traffic_pct'].clip(0, 100)

# 4. Map Weather
# Group weather into clear, rain, config mappings
def map_weather(w):
    w = str(w).lower()
    if 'rain' in w or 'drizzle' in w: return 1  # 1 = Rain
    if 'thunder' in w: return 2                 # 2 = Thunderstorm
    if 'fog' in w or 'mist' in w: return 3      # 3 = Fog
    return 0                                    # 0 = Clear/Cloudy

df['weather_code'] = df['weather_main'].apply(map_weather)

# 5. Map Holidays
df['is_holiday'] = (df['holiday'] != 'None').astype(int)

# 6. Synthesize Bengaluru Zones
# The raw dataset lacks "Zones". We will replicate the core data 4 times to represent
# the 4 specific Bengaluru traffic zones, injecting artificial variance to teach the model.
print("Synthesizing Bengaluru Zone profiles...")

# We will sample 10,000 rows to keep training fast, and multiply by 4 = 40,000 rows
base_sample = df.sample(n=min(10000, len(df)), random_state=42).copy()

zone_data = []

# Zone 0: IT Corridor (Massive spikes at 9am, 6pm)
df_it = base_sample.copy()
df_it['zone_id'] = 0
spike_mask = df_it['hour'].isin([8, 9, 10, 17, 18, 19]) & (df_it['day_of_week'] < 5)
df_it.loc[spike_mask, 'traffic_pct'] *= 1.35
zone_data.append(df_it)

# Zone 1: Commercial (High all day, massive evening peak)
df_com = base_sample.copy()
df_com['zone_id'] = 1
df_com.loc[(df_com['hour'] >= 11) & (df_com['hour'] <= 22), 'traffic_pct'] *= 1.15
zone_data.append(df_com)

# Zone 2: Residential (Morning outflow, evening inflow)
df_res = base_sample.copy()
df_res['zone_id'] = 2
df_res.loc[(df_res['hour'] >= 7) & (df_res['hour'] <= 10), 'traffic_pct'] *= 1.2
df_res.loc[(df_res['hour'] >= 16) & (df_res['hour'] <= 20), 'traffic_pct'] *= 1.25
zone_data.append(df_res)

# Zone 3: Mixed
df_mix = base_sample.copy()
df_mix['zone_id'] = 3
df_mix['traffic_pct'] *= 0.95
zone_data.append(df_mix)

# Combine
final_df = pd.concat(zone_data, ignore_index=True)
final_df['traffic_pct'] = final_df['traffic_pct'].clip(2, 98)

# 7. Final Features and Target
FEATURES = ['hour', 'day_of_week', 'zone_id', 'weather_code', 'is_holiday']
X = final_df[FEATURES]
y = final_df['traffic_pct']

# 8. Train the Machine Learning Model
print(f"Training RandomForestRegressor on {len(X)} rows...")
model = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
model.fit(X, y)

# 9. Save the Model
model_file = "traffic_model.pkl"
joblib.dump(model, model_file)
print(f"Success! Trained model saved to '{model_file}'.")
print("We can now run inference natively loaded via scikit-learn in app.py!")
