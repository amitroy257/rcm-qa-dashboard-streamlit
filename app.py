"""
Commure RCM Claims QA Dashboard
Built by Amit Bikram Roy | Data Operations Analyst Portfolio Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Commure RCM QA Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Professional Healthcare Blue/Green
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f3c 50%, #091a2e 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #091a2e 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.2);
}
[data-testid="stSidebar"] .css-1d391kg { padding-top: 2rem; }

/* ── Top Header ── */
.main-header {
    background: linear-gradient(135deg, #0369a1 0%, #0891b2 50%, #059669 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(3, 105, 161, 0.4);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}
.main-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.main-header p {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    margin: 0.3rem 0 0 0;
    font-weight: 400;
}
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    color: #fff;
    margin-top: 0.5rem;
    border: 1px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    backdrop-filter: blur(10px);
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(56, 189, 248, 0.2);
}
.kpi-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
    font-weight: 500;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.2rem;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: 0.03em;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
}

/* ── QA Check Cards ── */
.qa-pass {
    background: linear-gradient(135deg, rgba(5, 150, 105, 0.15), rgba(5, 150, 105, 0.05));
    border: 1px solid rgba(52, 211, 153, 0.4);
    border-left: 4px solid #34d399;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.qa-fail {
    background: linear-gradient(135deg, rgba(220, 38, 38, 0.15), rgba(220, 38, 38, 0.05));
    border: 1px solid rgba(252, 165, 165, 0.4);
    border-left: 4px solid #f87171;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.qa-warn {
    background: linear-gradient(135deg, rgba(217, 119, 6, 0.15), rgba(217, 119, 6, 0.05));
    border: 1px solid rgba(251, 191, 36, 0.4);
    border-left: 4px solid #fbbf24;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.qa-title { font-weight: 600; font-size: 0.95rem; color: #e2e8f0; }
.qa-detail { font-size: 0.83rem; color: #94a3b8; margin-top: 0.2rem; }

/* ── Process Steps ── */
.step-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.6rem 0;
    position: relative;
}
.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #0369a1, #0891b2);
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    color: #fff;
    margin-right: 0.6rem;
    flex-shrink: 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    color: #94a3b8;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0369a1, #0891b2) !important;
    color: white !important;
}

/* ── Tables ── */
.dataframe { font-size: 0.82rem !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(56, 189, 248, 0.15);
    color: #475569;
    font-size: 0.8rem;
}
.footer span { color: #38bdf8; }

/* ── Plotly charts transparent bg ── */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .svg-container {
    background: transparent !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #0369a1, #0891b2);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.2rem;
    transition: all 0.2s;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0284c7, #06b6d4);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(3, 105, 161, 0.4);
}

/* ── Metrics override ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART THEME DEFAULTS
# ─────────────────────────────────────────────
CHART_TEMPLATE = "plotly_dark"
CHART_COLORS = ["#38bdf8", "#34d399", "#a78bfa", "#fb923c", "#f472b6", "#facc15", "#4ade80"]
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"

def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="Inter", color="#94a3b8", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", showline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", showline=False)
    return fig

# ─────────────────────────────────────────────
#  DATA LOADING & SYNTHETIC FALLBACK
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load claims.csv or generate a realistic synthetic dataset."""
    try:
        df = pd.read_csv("claims.csv")
        # Normalise column names (strip spaces, title-case)
        df.columns = [c.strip() for c in df.columns]
        return df, "real"
    except FileNotFoundError:
        return generate_synthetic_data(), "synthetic"

@st.cache_data
def generate_synthetic_data():
    np.random.seed(42)
    n = 2000

    providers = ["General Hospital", "City Clinic", "MedCare Partners",
                 "HealthFirst IPA", "Regional Medical Center", "Sunrise Health"]
    denial_reasons = [
        "Missing Authorization", "Coding Error", "Patient Not Eligible",
        "Duplicate Claim", "Service Not Covered", "Timely Filing Exceeded",
        "Invalid Modifier", None, None, None, None, None  # Nones → Paid claims
    ]
    statuses = ["Paid", "Denied", "Pending", "Adjusted"]
    payer = ["Aetna", "BCBS", "Cigna", "UnitedHealth", "Medicare", "Medicaid"]
    cpt_codes = ["99213", "99214", "93000", "70553", "36415", "99232", "27447"]
    icd_codes = ["Z00.00", "I10", "E11.9", "J06.9", "M54.5", "F41.1", "K21.0"]

    claim_dates = pd.date_range("2023-01-01", "2024-06-30", periods=n)
    charge_amounts = np.random.uniform(150, 8500, n).round(2)
    
    # Status-based payments
    statuses_arr = np.random.choice(statuses, n, p=[0.62, 0.22, 0.10, 0.06])
    payment_amounts = []
    denial_reasons_arr = []
    
    for i, s in enumerate(statuses_arr):
        if s == "Paid":
            payment_amounts.append(round(charge_amounts[i] * np.random.uniform(0.7, 0.98), 2))
            denial_reasons_arr.append(None)
        elif s == "Denied":
            payment_amounts.append(0.0)
            denial_reasons_arr.append(np.random.choice(denial_reasons[:7]))
        elif s == "Pending":
            payment_amounts.append(0.0)
            denial_reasons_arr.append(None)
        else:  # Adjusted
            payment_amounts.append(round(charge_amounts[i] * np.random.uniform(0.4, 0.65), 2))
            denial_reasons_arr.append(np.random.choice(["Coding Error", "Invalid Modifier", None]))

    # Inject some QA issues
    ids = [f"CLM{str(i).zfill(6)}" for i in range(1, n + 1)]
    # Duplicates
    for idx in np.random.choice(range(n), 30, replace=False):
        ids[idx] = ids[max(0, idx - 1)]
    # Zero payments on paid claims
    for idx in np.random.choice(np.where(statuses_arr == "Paid")[0], 12, replace=False):
        payment_amounts[idx] = 0.0
    # Null values sprinkled in
    providers_arr = list(np.random.choice(providers, n))
    for idx in np.random.choice(range(n), 8, replace=False):
        providers_arr[idx] = None

    df = pd.DataFrame({
        "Claim_ID": ids,
        "Claim_Date": claim_dates.strftime("%Y-%m-%d"),
        "Provider": providers_arr,
        "Payer": np.random.choice(payer, n),
        "CPT_Code": np.random.choice(cpt_codes, n),
        "ICD_Code": np.random.choice(icd_codes, n),
        "Claim_Status": statuses_arr,
        "Denial_Reason": denial_reasons_arr,
        "Charge_Amount": charge_amounts,
        "Payment_Amount": payment_amounts,
        "Patient_Age": np.random.randint(1, 90, n),
        "Patient_Gender": np.random.choice(["M", "F"], n),
    })
    return df

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
df_raw, data_source = load_data()

# Ensure key columns exist with safe fallbacks
def ensure_col(df, col, default):
    if col not in df.columns:
        df[col] = default
    return df

df_raw = ensure_col(df_raw, "Claim_Status", "Unknown")
df_raw = ensure_col(df_raw, "Denial_Reason", None)
df_raw = ensure_col(df_raw, "Charge_Amount", 0.0)
df_raw = ensure_col(df_raw, "Payment_Amount", 0.0)

# Parse dates safely
for date_col in ["Claim_Date", "Service_Date", "Date"]:
    if date_col in df_raw.columns:
        df_raw[date_col] = pd.to_datetime(df_raw[date_col], errors="coerce")
        date_col_name = date_col
        break
else:
    df_raw["Claim_Date"] = pd.to_datetime("2023-01-01")
    date_col_name = "Claim_Date"

# ─────────────────────────────────────────────
#  SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family: Space Grotesk; font-size:1.1rem; font-weight:700; color:#38bdf8;'>🏥 RCM QA Dashboard</div>
        <div style='font-size:0.75rem; color:#475569; margin-top:0.2rem;'>Commure · Augmedix</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔧 Filters")

    # Claim Status filter
    statuses = ["All"] + sorted(df_raw["Claim_Status"].dropna().unique().tolist())
    sel_status = st.selectbox("Claim Status", statuses)

    # Denial Reason filter
    denial_vals = df_raw["Denial_Reason"].dropna().unique().tolist()
    if denial_vals:
        denial_opts = ["All"] + sorted(denial_vals)
        sel_denial = st.selectbox("Denial Reason", denial_opts)
    else:
        sel_denial = "All"

    # Provider filter
    provider_col = next((c for c in df_raw.columns if "provider" in c.lower()), None)
    if provider_col:
        providers_list = ["All"] + sorted(df_raw[provider_col].dropna().unique().tolist())
        sel_provider = st.selectbox("Provider", providers_list)
    else:
        sel_provider = "All"
        provider_col = None

    # Date range filter
    min_date = df_raw[date_col_name].min()
    max_date = df_raw[date_col_name].max()
    if pd.notna(min_date) and pd.notna(max_date):
        date_range = st.date_input(
            "Date Range",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date(),
        )
    else:
        date_range = None

    st.markdown("---")
    if data_source == "synthetic":
        st.info("📂 **Demo mode** — using synthetic data.\nAdd `claims.csv` to the folder to load real data.")
    else:
        st.success("✅ **Real data loaded** from `claims.csv`")

    st.markdown("""
    <div style='font-size:0.75rem; color:#475569; margin-top:1rem; line-height:1.6;'>
        Built by <span style='color:#38bdf8; font-weight:600;'>Amit Bikram Roy</span><br>
        Final-year CS · IUB Dhaka<br>
        🌙 Night-shift optimised
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = df_raw.copy()
if sel_status != "All":
    df = df[df["Claim_Status"] == sel_status]
if sel_denial != "All":
    df = df[df["Denial_Reason"] == sel_denial]
if provider_col and sel_provider != "All":
    df = df[df[provider_col] == sel_provider]
if date_range and len(date_range) == 2:
    d0, d1 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df[date_col_name] >= d0) & (df[date_col_name] <= d1)]

# ─────────────────────────────────────────────
#  MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏥 Commure RCM Claims QA Dashboard</h1>
    <p>Zero-error quality checks for Revenue Cycle Management · Built by <strong>Amit Bikram Roy</strong></p>
    <span class="badge">📊 Data Operations Analyst — Portfolio Project</span>
    <span class="badge" style="margin-left:8px;">🌙 Night-Shift Friendly</span>
    <span class="badge" style="margin-left:8px;">⚡ Real-Time Filters</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  COMPUTE KPIs
# ─────────────────────────────────────────────
total_claims = len(df)
denied = df[df["Claim_Status"].str.lower() == "denied"] if "Claim_Status" in df.columns else pd.DataFrame()
denial_rate = (len(denied) / total_claims * 100) if total_claims > 0 else 0

charge_col = next((c for c in df.columns if "charge" in c.lower()), None)
payment_col = next((c for c in df.columns if "payment" in c.lower() or "paid" in c.lower()), None)

if charge_col and payment_col:
    df[charge_col] = pd.to_numeric(df[charge_col], errors="coerce").fillna(0)
    df[payment_col] = pd.to_numeric(df[payment_col], errors="coerce").fillna(0)
    avg_payment_gap = (df[charge_col] - df[payment_col]).mean()
    total_charges = df[charge_col].sum()
    total_payments = df[payment_col].sum()
    collection_rate = (total_payments / total_charges * 100) if total_charges > 0 else 0
else:
    avg_payment_gap = 0
    total_charges = 0
    total_payments = 0
    collection_rate = 0

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Quality Checks", "📋 Process Guide"])

# ════════════════════════════════════════════
#  TAB 1 — DASHBOARD
# ════════════════════════════════════════════
with tab1:
    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{total_claims:,}</div>
            <div class="kpi-label">Total Claims</div>
            <div class="kpi-sub">After filters applied</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        color = "#f87171" if denial_rate > 20 else "#34d399"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number" style="color:{color};">{denial_rate:.1f}%</div>
            <div class="kpi-label">Denial Rate</div>
            <div class="kpi-sub">{'⚠ Above threshold' if denial_rate > 20 else '✓ Within target'}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">${avg_payment_gap:,.0f}</div>
            <div class="kpi-label">Avg Payment Gap</div>
            <div class="kpi-sub">Charge minus payment</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{collection_rate:.1f}%</div>
            <div class="kpi-label">Collection Rate</div>
            <div class="kpi-sub">${total_payments:,.0f} collected</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Claims by Provider | Denial Reasons Pie
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="section-header">Claims by Provider</div>', unsafe_allow_html=True)
        if provider_col and provider_col in df.columns:
            prov_data = df[provider_col].value_counts().head(8).reset_index()
            prov_data.columns = ["Provider", "Count"]
            fig_prov = px.bar(
                prov_data, x="Count", y="Provider", orientation="h",
                color="Count", color_continuous_scale=["#0369a1", "#38bdf8", "#34d399"],
                template=CHART_TEMPLATE,
            )
            fig_prov.update_traces(
                hovertemplate="<b>%{y}</b><br>Claims: %{x:,}<extra></extra>",
                marker_line_width=0,
            )
            fig_prov.update_layout(
                coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"),
                xaxis_title="", yaxis_title="",
            )
            st.plotly_chart(style_chart(fig_prov, 320), use_container_width=True)
        else:
            st.info("No Provider column found in data.")

    with col_b:
        st.markdown('<div class="section-header">Denial Reasons Breakdown</div>', unsafe_allow_html=True)
        denial_data = df["Denial_Reason"].dropna().value_counts().reset_index()
        denial_data.columns = ["Reason", "Count"]
        if len(denial_data) > 0:
            fig_pie = px.pie(
                denial_data.head(6), values="Count", names="Reason",
                color_discrete_sequence=CHART_COLORS, template=CHART_TEMPLATE,
                hole=0.45,
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>",
            )
            fig_pie.update_layout(
                showlegend=True,
                legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(style_chart(fig_pie, 320), use_container_width=True)
        else:
            st.success("✅ No denials found in current filter selection.")

    # Row 2: Monthly trend | Status Distribution
    col_c, col_d = st.columns([3, 2])

    with col_c:
        st.markdown('<div class="section-header">Monthly Claims Trend</div>', unsafe_allow_html=True)
        df["Month"] = df[date_col_name].dt.to_period("M").astype(str)
        monthly = df.groupby(["Month", "Claim_Status"]).size().reset_index(name="Count")
        monthly = monthly.sort_values("Month")
        if len(monthly) > 0:
            fig_line = px.line(
                monthly, x="Month", y="Count", color="Claim_Status",
                color_discrete_sequence=CHART_COLORS, template=CHART_TEMPLATE,
                markers=True,
            )
            fig_line.update_traces(line_width=2.5, marker_size=5)
            fig_line.update_layout(xaxis_title="", yaxis_title="Claims", legend_title="")
            st.plotly_chart(style_chart(fig_line, 320), use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Claim Status Distribution</div>', unsafe_allow_html=True)
        status_data = df["Claim_Status"].value_counts().reset_index()
        status_data.columns = ["Status", "Count"]
        fig_bar = px.bar(
            status_data, x="Status", y="Count",
            color="Status", color_discrete_sequence=CHART_COLORS,
            template=CHART_TEMPLATE,
        )
        fig_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>%{y:,} claims<extra></extra>",
            marker_line_width=0,
        )
        fig_bar.update_layout(showlegend=False, xaxis_title="", yaxis_title="")
        st.plotly_chart(style_chart(fig_bar, 320), use_container_width=True)

    # Download filtered CSV
    st.markdown("---")
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(
        label="⬇️  Download Filtered Claims as CSV",
        data=csv_buf.getvalue(),
        file_name=f"rcm_claims_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

# ════════════════════════════════════════════
#  TAB 2 — QUALITY CHECKS
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🔍 Automated QA Checks — SQL-Style Validation</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b; font-size:0.88rem; margin-bottom:1.5rem;'>"
        "Each check mirrors a real SQL query run against the claims dataset. "
        "These are the same validations run nightly on Commure's RCM pipelines.</p>",
        unsafe_allow_html=True
    )

    # ── CHECK 1: Duplicate Claim IDs
    claim_id_col = next((c for c in df_raw.columns if "claim_id" in c.lower() or "id" == c.lower()), None)
    if claim_id_col:
        dupes = df_raw[df_raw.duplicated(subset=[claim_id_col], keep=False)]
        dupe_count = df_raw[claim_id_col].duplicated().sum()
        status_class = "qa-fail" if dupe_count > 0 else "qa-pass"
        icon = "🔴" if dupe_count > 0 else "🟢"
        st.markdown(f"""
        <div class="{status_class}">
            <div class="qa-title">{icon} CHECK 1 — Duplicate Claim IDs</div>
            <div class="qa-detail">SQL equivalent: <code>SELECT Claim_ID, COUNT(*) FROM claims GROUP BY Claim_ID HAVING COUNT(*) > 1</code></div>
            <div class="qa-detail" style="margin-top:0.4rem;">
                <strong>Result:</strong> {dupe_count} duplicate Claim IDs found out of {len(df_raw):,} total records.
            </div>
        </div>""", unsafe_allow_html=True)
        if dupe_count > 0 and len(dupes) > 0:
            with st.expander(f"View {min(dupe_count, 10)} sample duplicates"):
                st.dataframe(dupes.head(10), use_container_width=True)
    else:
        st.markdown('<div class="qa-warn"><div class="qa-title">⚠️ CHECK 1 — No Claim ID column found</div></div>', unsafe_allow_html=True)

    # ── CHECK 2: Paid claims with $0 payment
    if payment_col:
        paid_mask = df_raw["Claim_Status"].str.lower() == "paid"
        zero_paid = df_raw[paid_mask & (df_raw[payment_col] == 0)]
        cnt = len(zero_paid)
        status_class = "qa-fail" if cnt > 0 else "qa-pass"
        icon = "🔴" if cnt > 0 else "🟢"
        st.markdown(f"""
        <div class="{status_class}">
            <div class="qa-title">{icon} CHECK 2 — Paid Claims with Zero Payment Amount</div>
            <div class="qa-detail">SQL equivalent: <code>SELECT * FROM claims WHERE Claim_Status = 'Paid' AND Payment_Amount = 0</code></div>
            <div class="qa-detail" style="margin-top:0.4rem;">
                <strong>Result:</strong> {cnt} claims marked 'Paid' but have $0 payment.
            </div>
        </div>""", unsafe_allow_html=True)
        if cnt > 0:
            with st.expander(f"View {min(cnt, 10)} sample anomalies"):
                st.dataframe(zero_paid.head(10), use_container_width=True)

    # ── CHECK 3: Charge vs Payment mismatch (payment > charge)
    if charge_col and payment_col:
        overpaid = df_raw[df_raw[payment_col] > df_raw[charge_col]]
        cnt = len(overpaid)
        status_class = "qa-fail" if cnt > 0 else "qa-pass"
        icon = "🔴" if cnt > 0 else "🟢"
        st.markdown(f"""
        <div class="{status_class}">
            <div class="qa-title">{icon} CHECK 3 — Payment Exceeds Charge Amount</div>
            <div class="qa-detail">SQL equivalent: <code>SELECT * FROM claims WHERE Payment_Amount > Charge_Amount</code></div>
            <div class="qa-detail" style="margin-top:0.4rem;">
                <strong>Result:</strong> {cnt} records where payment is higher than the billed charge — possible data entry error.
            </div>
        </div>""", unsafe_allow_html=True)
        if cnt > 0:
            with st.expander("View sample"):
                st.dataframe(overpaid.head(10), use_container_width=True)

    # ── CHECK 4: Null / missing values
    null_counts = df_raw.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    has_nulls = len(null_cols) > 0
    status_class = "qa-warn" if has_nulls else "qa-pass"
    icon = "🟡" if has_nulls else "🟢"
    null_summary = ", ".join([f"{c}: {v}" for c, v in null_cols.items()]) if has_nulls else "None"
    st.markdown(f"""
    <div class="{status_class}">
        <div class="qa-title">{icon} CHECK 4 — Null / Missing Values Audit</div>
        <div class="qa-detail">SQL equivalent: <code>SELECT column_name, COUNT(*) FROM claims WHERE column_name IS NULL</code></div>
        <div class="qa-detail" style="margin-top:0.4rem;">
            <strong>Columns with nulls:</strong> {null_summary}
        </div>
    </div>""", unsafe_allow_html=True)

    # ── CHECK 5: Top Denial Reasons + volume
    st.markdown('<div class="section-header" style="margin-top:1.5rem;">Top Denial Reasons — Frequency Table</div>', unsafe_allow_html=True)
    denial_summary = df_raw["Denial_Reason"].dropna().value_counts().reset_index()
    denial_summary.columns = ["Denial Reason", "Count"]
    denial_summary["% of Denials"] = (denial_summary["Count"] / denial_summary["Count"].sum() * 100).round(1).astype(str) + "%"
    denial_summary["Action Required"] = denial_summary["Denial Reason"].map({
        "Missing Authorization": "🔴 Contact Utilization Management",
        "Coding Error": "🔴 Rebill with corrected codes",
        "Patient Not Eligible": "🟡 Verify eligibility pre-service",
        "Duplicate Claim": "🟡 Check claim submission logs",
        "Service Not Covered": "⚪ Review payer policy",
        "Timely Filing Exceeded": "🔴 Submit appeal immediately",
        "Invalid Modifier": "🔴 Rebill with correct modifier",
    }).fillna("🟢 Review and appeal")

    if len(denial_summary) > 0:
        st.dataframe(
            denial_summary,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("✅ No denials in the current filtered view.")

    # ── QA Summary scorecard
    st.markdown('<div class="section-header" style="margin-top:1.5rem;">QA Summary Scorecard</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    dupe_count_safe = dupe_count if claim_id_col else 0
    zero_paid_count = cnt if payment_col else 0
    with sc1:
        st.metric("Duplicate IDs", dupe_count_safe, delta=f"-{dupe_count_safe} to fix" if dupe_count_safe else "✓ Clean", delta_color="inverse")
    with sc2:
        st.metric("Paid / $0 Payment", zero_paid_count, delta=f"-{zero_paid_count} to fix" if zero_paid_count else "✓ Clean", delta_color="inverse")
    with sc3:
        st.metric("Null Fields", int(null_cols.sum()), delta="Review needed" if has_nulls else "✓ Clean", delta_color="inverse")
    with sc4:
        st.metric("Denial Rate", f"{denial_rate:.1f}%", delta="High" if denial_rate > 20 else "✓ Normal", delta_color="inverse")

# ════════════════════════════════════════════
#  TAB 3 — PROCESS GUIDE
# ════════════════════════════════════════════
with tab3:
    col_guide, col_down = st.columns([2, 1])

    with col_guide:
        st.markdown('<div class="section-header">📋 RCM Claims QA Process — Standard Operating Procedure</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style='color:#64748b; font-size:0.88rem;'>
        This SOP mirrors the daily workflow for a Data Operations Analyst on Commure's RCM Global team.
        Follow these steps at the start of each night shift.
        </p>
        """, unsafe_allow_html=True)

        steps = [
            ("Pre-Shift Setup", [
                "Log into the RCM data portal and confirm VPN connection is active.",
                "Download the latest claims batch file (CSV) from the SFTP server.",
                "Load the file into the QA Dashboard — verify row count matches the expected batch size.",
                "Check the date range on loaded claims matches tonight's processing window.",
            ]),
            ("Data Integrity Checks", [
                "Run CHECK 1: Identify all duplicate Claim_IDs using GROUP BY + HAVING COUNT(*) > 1.",
                "Run CHECK 2: Flag all 'Paid' status claims with Payment_Amount = 0.",
                "Run CHECK 3: Detect over-payments where Payment_Amount > Charge_Amount.",
                "Run CHECK 4: Generate null value report for all key fields (Provider, Payer, CPT Code).",
                "Document all findings in the QA Exception Log with timestamp and claim count.",
            ]),
            ("Denial Analysis", [
                "Filter to Denied claims only. Export denial summary grouped by Denial_Reason.",
                "Cross-reference denial codes with payer-specific coding guidelines.",
                "Escalate 'Timely Filing Exceeded' and 'Missing Authorization' cases immediately to the supervisor.",
                "Prepare appeal queue for Coding Error and Invalid Modifier denials.",
            ]),
            ("Reporting & Handoff", [
                "Export the filtered clean report as CSV using the download button.",
                "Update the shift summary dashboard with tonight's Denial Rate, Collection Rate, and QA issues.",
                "Post the nightly QA summary in the team Slack channel before 6:00 AM.",
                "Hand off any unresolved exceptions to the morning team with full context notes.",
            ]),
            ("Continuous Improvement", [
                "Log recurring denial patterns in the weekly trends tracker (Excel/Power BI).",
                "Suggest coding rule updates to reduce repeat errors.",
                "Attend weekly QA debrief — bring 3 data points to support your process improvement idea.",
            ]),
        ]

        for i, (title, items) in enumerate(steps, 1):
            st.markdown(f"""
            <div class="step-box">
                <div style="display:flex; align-items:center; margin-bottom:0.6rem;">
                    <span class="step-number">{i}</span>
                    <span style="font-family:'Space Grotesk'; font-weight:600; font-size:0.95rem; color:#e2e8f0;">{title}</span>
                </div>
                <ul style="margin:0; padding-left:1.2rem; color:#94a3b8; font-size:0.85rem; line-height:1.8;">
                    {"".join(f"<li>{item}</li>" for item in items)}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with col_down:
        st.markdown('<div class="section-header">📥 Download Reports</div>', unsafe_allow_html=True)

        # Clean report — rows with no null in key fields
        key_cols = [c for c in ["Claim_ID", "Claim_Status", "Charge_Amount", "Payment_Amount", "Provider"] if c in df.columns]
        df_clean = df.dropna(subset=key_cols) if key_cols else df.copy()
        if claim_id_col:
            df_clean = df_clean[~df_clean[claim_id_col].duplicated(keep="first")]

        clean_buf = io.StringIO()
        df_clean.to_csv(clean_buf, index=False)
        st.download_button(
            label="⬇️  Download Clean Report (CSV)",
            data=clean_buf.getvalue(),
            file_name=f"rcm_clean_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # QA exceptions report
        exceptions = []
        if claim_id_col and dupe_count_safe > 0:
            dup_df = df_raw[df_raw.duplicated(subset=[claim_id_col], keep=False)].copy()
            dup_df["QA_Flag"] = "Duplicate Claim_ID"
            exceptions.append(dup_df)
        if payment_col:
            paid_mask = df_raw["Claim_Status"].str.lower() == "paid"
            zp = df_raw[paid_mask & (df_raw[payment_col] == 0)].copy()
            if len(zp) > 0:
                zp["QA_Flag"] = "Paid / Zero Payment"
                exceptions.append(zp)

        if exceptions:
            exc_df = pd.concat(exceptions).drop_duplicates()
            exc_buf = io.StringIO()
            exc_df.to_csv(exc_buf, index=False)
            st.download_button(
                label="⬇️  Download QA Exceptions (CSV)",
                data=exc_buf.getvalue(),
                file_name=f"rcm_qa_exceptions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:10px; padding:1rem; font-size:0.82rem; color:#94a3b8;">
            <div style="font-weight:600; color:#38bdf8; margin-bottom:0.5rem;">📌 Quick Reference</div>
            <div>• Denial Rate target: <strong style='color:#34d399;'>&lt; 15%</strong></div>
            <div>• Collection Rate target: <strong style='color:#34d399;'>&gt; 85%</strong></div>
            <div>• Zero duplicates tolerance: <strong style='color:#f87171;'>0</strong></div>
            <div>• Null fields tolerance: <strong style='color:#fbbf24;'>&lt; 0.1%</strong></div>
            <div style="margin-top:0.6rem;">Night shift window: <strong>10 PM – 7 AM BST</strong></div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built in 1 evening &nbsp;•&nbsp; Night-shift friendly &nbsp;•&nbsp;
    <span>Python + Streamlit + Plotly</span> &nbsp;•&nbsp;
    <span>Amit Bikram Roy</span> · Final-year CS · IUB Dhaka &nbsp;•&nbsp;
    Portfolio project for <span>Commure / Augmedix</span> Data Operations Analyst Role
</div>
""", unsafe_allow_html=True)
