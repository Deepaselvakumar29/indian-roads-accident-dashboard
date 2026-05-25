# 🚦 Indian Roads Accident Analysis Dashboard

An interactive dashboard to explore and analyze **20,000 Indian road accident records** using Streamlit and Plotly.

---

## 📁 Files Included

```
indian_roads_project/
├── app.py                      # Main dashboard (run this)
├── preprocess.py               # Data cleaning module
├── indian_roads_dataset.xlsx   # Dataset (20,000 records)
├── requirements.txt            # Dependencies list
└── README.md                   # This file
```

---

## ⚙️ Requirements

- Python 3.9 or above
- Internet connection (for first-time package install)

---

## 🚀 How to Run

### Step 1 — Open Command Prompt (CMD)

Press `Win + R` → type `cmd` → Enter

### Step 2 — Go to Project Folder

```bash
cd path\to\indian_roads_project
```

Example:
```bash
cd D:\indian_roads_project
```

### Step 3 — Install Required Packages

```bash
pip install streamlit pandas plotly openpyxl numpy==1.24.3
```

> ⏳ This may take 2–3 minutes. Run only once.

### Step 4 — Run the Dashboard

```bash
python -m streamlit run app.py
```

### Step 5 — View in Browser

The dashboard will automatically open at:

```
http://localhost:8501
```

If it does not open automatically, copy the above link and paste it in your browser.

---

## 📊 Dashboard Features

| Section | Description |
|--------|-------------|
| 📈 KPI Cards | Total accidents, casualties, fatal %, avg risk score |
| 🥧 Severity Chart | Minor / Major / Fatal breakdown |
| 🎯 Cause Analysis | Top accident causes |
| 📅 Monthly Trend | Severity split across months |
| 🕐 Hourly Pattern | Accident count by hour of day |
| 🗺️ State-wise Chart | Stacked bar by state and severity |
| 🌤️ Weather Impact | Weather vs accident severity |
| 🛣️ Road Type Analysis | Accidents vs casualties by road type |
| 📊 Risk Distribution | Risk score histogram |
| 📆 Day-of-Week | Weekday vs weekend comparison |
| 🎉 Festival Analysis | Accidents during festivals |
| 🗺️ India Map | Interactive geospatial accident map |
| 📋 Data Table | Filtered data with CSV download |

---

## 🔍 Sidebar Filters

All charts update dynamically based on:
- State & City
- Accident Severity
- Road Type
- Weather Condition
- Year Range

---

## 🧹 Data Cleaning Applied

| Step | Action |
|------|--------|
| Missing values | festival NaN filled as No Festival |
| Date features | Extracted year, month, month_name |
| Severity encoding | minor=1, major=2, fatal=3 |
| Risk category | Low / Medium / High from risk score |
| Time of day | Morning / Afternoon / Evening / Night |
| Duplicates | Checked and removed duplicate accident IDs |
| Data types | Optimised all categoricals to category dtype |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Dashboard framework |
| Plotly | Interactive charts & map |
| Pandas | Data manipulation |
| OpenPyXL | Excel file reading |

---

*Built as part of Indian Roads Accident Data Analysis Project.*
