# 🚦 Indian Roads Accident Analysis Dashboard

An interactive Streamlit dashboard for exploring and analyzing the Indian Roads Accident dataset.

## 📁 Project Structure

```
indian_roads_project/
├── app.py                    # Streamlit dashboard (main entry point)
├── preprocess.py             # Data cleaning & preprocessing module
├── indian_roads_dataset.xlsx # Raw dataset (20,000 records)
├── requirements.txt          # Python dependencies
└── README.md
```

## 🛠️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**

## 🧹 Data Cleaning Steps (preprocess.py)

| Step | Action |
|------|--------|
| Missing values | `festival` NaN → `'No Festival'` |
| Date parsing | Extracted `year`, `month`, `month_name` |
| Severity encoding | `minor=1`, `major=2`, `fatal=3` |
| Risk categorisation | `Low / Medium / High` from `risk_score` |
| Time of day | `Morning / Afternoon / Evening / Night` |
| Deduplication | Removed duplicate `accident_id` rows |
| Data types | All categoricals cast to `category` dtype |

## 📊 Dashboard Features

- **7 KPI cards** — Total accidents, casualties, vehicles, fatal %, avg risk, peak hour %, weekend %
- **Severity pie chart** — Minor / Major / Fatal breakdown
- **Cause bar chart** — Top accident causes
- **Monthly trend lines** — Severity split across months
- **Hourly heatmap** — Accident distribution by hour
- **State-wise stacked bar** — City-level severity comparison
- **Weather impact chart** — Weather vs severity cross-analysis
- **Road type scatter** — Accidents vs casualties vs avg risk
- **Risk score histogram** — Distribution by severity
- **Day-of-week bar** — Weekday vs weekend highlighting
- **Festival analysis** — Accident count during festivals
- **Interactive map** — Geospatial scatter with hover details
- **Data table + CSV download** — Filtered data export

## 🔍 Sidebar Filters

All charts respond to:
- State / City
- Accident Severity (multi-select)
- Road Type (multi-select)
- Weather (multi-select)
- Year Range (slider)

## 📦 Key Libraries

- `streamlit` — Dashboard framework
- `plotly` — Interactive charts & maps
- `pandas` — Data manipulation
- `openpyxl` — Excel file reading
