"""
Indian Roads Accident Dataset - Data Cleaning & Preprocessing
"""

import pandas as pd
import numpy as np
import os

def load_and_clean(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)

    # ── 1. Festival: fill NaN → 'No Festival' ──────────────────────────────
    df['festival'] = df['festival'].fillna('No Festival')

    # ── 2. Date & time cleanup ─────────────────────────────────────────────
    df['date'] = pd.to_datetime(df['date'])
    df['year']  = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%b')

    # ── 3. Ordinal encoding for severity ──────────────────────────────────
    severity_map = {'minor': 1, 'major': 2, 'fatal': 3}
    df['severity_code'] = df['accident_severity'].map(severity_map)

    # ── 4. Visibility: standardise case ────────────────────────────────────
    df['visibility'] = df['visibility'].str.strip().str.lower()

    # ── 5. Risk category from risk_score ──────────────────────────────────
    df['risk_category'] = pd.cut(
        df['risk_score'],
        bins=[0, 0.33, 0.66, 1.01],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )

    # ── 6. Time of day ─────────────────────────────────────────────────────
    def time_of_day(h):
        if 5 <= h < 12:   return 'Morning'
        elif 12 <= h < 17: return 'Afternoon'
        elif 17 <= h < 21: return 'Evening'
        else:              return 'Night'
    df['time_of_day'] = df['hour'].apply(time_of_day)

    # ── 7. Drop duplicate accident_ids ────────────────────────────────────
    before = len(df)
    df = df.drop_duplicates(subset='accident_id')
    after = len(df)
    if before != after:
        print(f"[preprocess] Removed {before-after} duplicate rows")

    # ── 8. Ensure correct dtypes ──────────────────────────────────────────
    cat_cols = ['city','state','road_type','weather','visibility',
                'traffic_density','cause','accident_severity',
                'day_of_week','festival','risk_category','time_of_day']
    for c in cat_cols:
        df[c] = df[c].astype('category')

    df = df.reset_index(drop=True)
    print(f"[preprocess] Clean dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    return {
        "total_accidents": len(df),
        "total_casualties": int(df['casualties'].sum()),
        "total_vehicles":   int(df['vehicles_involved'].sum()),
        "fatal_pct":        round(df['accident_severity'].eq('fatal').mean() * 100, 1),
        "avg_risk":         round(df['risk_score'].mean(), 3),
        "peak_hour_pct":    round(df['is_peak_hour'].mean() * 100, 1),
        "weekend_pct":      round(df['is_weekend'].mean() * 100, 1),
    }


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    df = load_and_clean(os.path.join(base, "indian_roads_dataset.xlsx"))
    out = os.path.join(base, "cleaned_data.csv")
    df.to_csv(out, index=False)
    print(f"[preprocess] Saved → {out}")
    print(get_summary_stats(df))
