# 🏥 Commure RCM Claims QA Dashboard
# Live Website :  https://rcm-app-dashboard-app.streamlit.app/
> **Zero-error quality checks for Revenue Cycle Management**  
> Built by **Amit Bikram Roy** · Final-year CS @ IUB Dhaka  
> Portfolio project for **Data Operations Analyst** — Commure / Augmedix

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://rcm-app-dashboard-app.streamlit.app/)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-purple)

---

## 📸 What It Looks Like

The dashboard has **3 tabs**:

| Tab | What you see |
|-----|-------------|
| 📊 Dashboard | KPI cards (Denial Rate, Avg Payment Gap, Collection Rate), bar/pie/line Plotly charts, filterable by Status / Denial Reason / Provider / Date |
| 🔍 Quality Checks | 5 automated SQL-style validations — duplicate IDs, zero payments, overpayments, null fields, denial frequency table |
| 📋 Process Guide | 5-step RCM SOP written like a real internal doc + CSV download buttons for clean data and QA exceptions |

---

## 🚀 Run Locally (2 minutes)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/rcm-qa-dashboard-streamlit.git
cd rcm-qa-dashboard-streamlit
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add data (optional)
- Download the dataset from [Kaggle — Synthetic Healthcare Claims](https://www.kaggle.com/datasets/abuthahir1998/synthetic-healthcare-claims-dataset)
- Save the CSV as **`claims.csv`** in the same folder as `app.py`
- If no file is found, the app runs on a **built-in synthetic demo dataset** automatically — no setup needed

### 5. Launch the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` ✅

---

## ☁️ Deploy Free on Streamlit Cloud

1. Push this repo to GitHub (use the name `rcm-qa-dashboard-streamlit`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Connect your GitHub account → select this repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** — your app is live in ~2 minutes 🎉

> **Tip:** If you want to include real data in your deployed app, commit `claims.csv` to the repo. Otherwise the synthetic data loads automatically and the app still looks great.

---

## 🗂 Project Structure

```
rcm-qa-dashboard-streamlit/
│
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── claims.csv          ← (Optional) Real/Kaggle claims data
└── README.md           ← This file
```

---

## 🔍 QA Checks Implemented

| # | Check | SQL Equivalent |
|---|-------|---------------|
| 1 | Duplicate Claim IDs | `GROUP BY Claim_ID HAVING COUNT(*) > 1` |
| 2 | Paid claims with $0 payment | `WHERE Status='Paid' AND Payment_Amount=0` |
| 3 | Payment exceeds charge | `WHERE Payment_Amount > Charge_Amount` |
| 4 | Null / missing fields | `WHERE column IS NULL` |
| 5 | Top denial reasons ranked | `GROUP BY Denial_Reason ORDER BY COUNT DESC` |

---

## 📊 Features

- **Real-time filters** — Claim Status, Denial Reason, Provider, Date range
- **Interactive charts** — Plotly bar, pie (donut), and line trend charts
- **Download buttons** — Filtered CSV, Clean Report, QA Exceptions Report
- **Dark mode UI** — Professional healthcare blue/green palette
- **Night-shift friendly** — Low-contrast dark theme, large readable KPIs
- **Synthetic fallback** — Works instantly without any external data

---

## 🎯 Why I Built This

The **Data Operations Analyst** role at Commure / Augmedix requires:
- ✅ SQL proficiency on large healthcare claims datasets
- ✅ Zero-error quality assurance mindset
- ✅ Building dashboards (Excel / Power BI / Google Sheets)
- ✅ Writing clear process documentation / SOPs
- ✅ Strong attention to detail + night-shift readiness

This project demonstrates all five requirements in a single live app.

---

## 👤 About Me

**Amit Bikram Roy**  
Final-year Computer Science student · Independent University Bangladesh, Dhaka  
SQL Champion | National Chess Player (FIDE 2064)

- 🏆 Database Project Showcase Champion
- 🌏 Research presented at international conference in Manila
- ♟️ President, IUB Chess Club | College Ambassador, Chess.com
- 🐍 Python · Pandas · NumPy · Matplotlib · Power BI · Excel

---

## 📄 License

MIT — free to use, adapt, and show in interviews.

---

Built in 1 evening
