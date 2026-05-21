import streamlit as st
import pandas as pd
import plotly.express as px
from prediction import render_prediction_page
from explainability import render_explainability_page
from chatbot import render_high_risk_explorer, render_executive_ai_assistant

st.set_page_config(
    page_title="CardioIntel AI",
    page_icon="🫀",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/heart_failure_dataset.csv")

df = load_data()

# =========================
# PREMIUM EXECUTIVE SIDEBAR
# =========================

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 55%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.25);
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-title {
        font-size: 30px;
        font-weight: 900;
        line-height: 1.15;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #38bdf8, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #cbd5e1;
        margin-bottom: 24px;
    }

    .sidebar-badge {
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #e0f2fe;
        padding: 10px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
    }

    .sidebar-section {
        font-size: 13px;
        font-weight: 800;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 22px;
        margin-bottom: 10px;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 14px;
        padding: 10px 12px;
        margin-bottom: 8px;
        transition: all 0.25s ease;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.45);
        transform: translateX(4px);
    }

    [data-testid="stMultiSelect"] {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 4px;
    }

    .sidebar-footer {
        margin-top: 28px;
        padding: 16px;
        border-radius: 18px;
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.30);
        font-size: 13px;
        color: #dcfce7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div class="sidebar-title">🫀 CardioIntel AI</div>
    <div class="sidebar-subtitle">
    Executive Cardiovascular Risk Intelligence & Explainable Healthcare AI Platform
    </div>
    <div class="sidebar-badge">
    🏥 Enterprise Clinical Command Center
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "🏥 Executive Overview",
        "📊 Clinical Analytics",
        "🚨 Risk Intelligence",
        "🏨 Hospital Operations",
        "🧬 Biomarker Intelligence",
        "🚨 High-Risk Patient Explorer",
        "🧠 Mortality AI Prediction",
        "🔍 Explainable AI Insights",
        "🤖 Executive Clinical AI Assistant",
        "💡 Executive Recommendations"
    ]
)

st.sidebar.markdown('<div class="sidebar-section">Executive Filters</div>', unsafe_allow_html=True)

hospital_filter = st.sidebar.selectbox(
    "🏥 Hospital Site",
    options=["All Hospitals"] + sorted(df["hospital_site"].unique().tolist())
)

risk_filter = st.sidebar.selectbox(
    "🚨 Risk Category",
    options=["All Risk Categories", "Low", "Moderate", "High", "Critical"]
)

if hospital_filter == "All Hospitals":
    hospital_selected = df["hospital_site"].unique()
else:
    hospital_selected = [hospital_filter]

if risk_filter == "All Risk Categories":
    risk_selected = df["risk_category"].unique()
else:
    risk_selected = [risk_filter]


filtered_df = df[
    (df["hospital_site"].isin(hospital_selected)) &
    (df["risk_category"].isin(risk_selected))
]
# =========================
# GLOBAL METRICS
# =========================
total_patients = len(filtered_df)
mortality_rate = filtered_df["DEATH_EVENT"].mean() * 100
readmission_rate = filtered_df["readmission_30d"].mean() * 100
icu_rate = filtered_df["icu_admission"].mean() * 100
avg_los = filtered_df["length_of_stay_days"].mean()
total_bed_days = filtered_df["length_of_stay_days"].sum()

st.markdown(
    """
    <style>
    /* APP BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%);
    }

    /* MAIN TITLE */
    .main-title {
        font-size: 46px;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 18px;
        color: #475569;
        margin-bottom: 12px;
    }

    /* SECTION HEADERS */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 800;
    }

    /* KPI CARDS */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.92);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.25);
        box-shadow: 0 10px 25px rgba(15,23,42,0.08);
    }

    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 900;
        color: #0f172a;
    }

    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 700;
        color: #475569;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 55%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.25);
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-title {
        font-size: 31px;
        font-weight: 900;
        line-height: 1.12;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #38bdf8, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #cbd5e1;
        margin-bottom: 18px;
        line-height: 1.45;
    }

    .sidebar-badge {
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #e0f2fe;
        padding: 10px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 20px;
        text-align: center;
    }

    .sidebar-section {
        font-size: 12px;
        font-weight: 900;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.055);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 15px;
        padding: 10px 12px;
        margin-bottom: 8px;
        transition: all 0.25s ease;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.50);
        transform: translateX(4px);
    }

    /* SELECTBOX FIX */
    [data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 14px !important;
    }

    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] input {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    [data-baseweb="select"] svg {
        color: #111827 !important;
        fill: #111827 !important;
    }

    /* INSIGHT BOXES */
    .insight-box {
        background: linear-gradient(135deg, #eff6ff, #ffffff);
        padding: 20px;
        border-radius: 18px;
        border-left: 7px solid #2563eb;
        box-shadow: 0 8px 20px rgba(37,99,235,0.08);
        margin-bottom: 15px;
        color: #0f172a;
    }

    .recommend-box {
        background: linear-gradient(135deg, #ecfdf5, #ffffff);
        padding: 20px;
        border-radius: 18px;
        border-left: 7px solid #16a34a;
        box-shadow: 0 8px 20px rgba(22,163,74,0.08);
        margin-bottom: 15px;
        color: #0f172a;
    }

    /* PLOT CONTAINERS */
    [data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.82);
        border-radius: 20px;
        padding: 10px;
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow: 0 8px 22px rgba(15,23,42,0.06);
    }

    /* FOOTER */
    .executive-footer {
        margin-top: 35px;
        padding: 16px 20px;
        border-radius: 18px;
        background: #0f172a;
        color: #e2e8f0;
        font-size: 13px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🫀 CardioIntel AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Executive Cardiovascular Risk Intelligence & Explainable Healthcare AI Platform</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# PAGE 1
# =========================
if page == "🏥 Executive Overview":

    st.subheader("🏥 Executive Overview Dashboard")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Patients", f"{total_patients:,}")
    col2.metric("Mortality Rate", f"{mortality_rate:.2f}%")
    col3.metric("30-Day Readmission", f"{readmission_rate:.2f}%")
    col4.metric("ICU Admission", f"{icu_rate:.2f}%")
    col5.metric("Avg LOS", f"{avg_los:.2f} days")

    st.markdown("### 📊 Executive Intelligence Visuals")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(
            filtered_df,
            names="DEATH_EVENT",
            title="Mortality Distribution",
            hole=0.45
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.histogram(
            filtered_df,
            x="risk_category",
            title="Risk Category Distribution",
            color="risk_category"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Quantified Executive Insights")

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Mortality burden:</b> {mortality_rate:.2f}% across {total_patients:,} patients, representing approximately 
        <b>{int(filtered_df['DEATH_EVENT'].sum()):,}</b> mortality events.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Readmission burden:</b> {readmission_rate:.2f}% 30-day readmission rate, representing approximately 
        <b>{int(filtered_df['readmission_30d'].sum()):,}</b> repeat admission events.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Operational load:</b> Average LOS is {avg_los:.2f} days, generating approximately 
        <b>{int(total_bed_days):,}</b> total inpatient bed-days.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# PAGE 2
# =========================
elif page == "📊 Clinical Analytics":

    st.subheader("📊 Clinical Analytics")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            filtered_df,
            x="nyha_class",
            color="nyha_class",
            title="NYHA Class Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.histogram(
            filtered_df,
            x="hf_phenotype",
            color="hf_phenotype",
            title="Heart Failure Phenotype Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    mortality_by_nyha = filtered_df.groupby("nyha_class")["DEATH_EVENT"].mean().reset_index()
    mortality_by_nyha["DEATH_EVENT"] *= 100

    fig = px.bar(
        mortality_by_nyha,
        x="nyha_class",
        y="DEATH_EVENT",
        title="Mortality Rate by NYHA Class",
        labels={"DEATH_EVENT": "Mortality Rate (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Quantified Clinical Insights")

    highest_nyha = mortality_by_nyha.sort_values("DEATH_EVENT", ascending=False).iloc[0]

    st.markdown(
        f"""
        <div class="insight-box">
        <b>NYHA Class {int(highest_nyha['nyha_class'])}</b> has the highest mortality burden at 
        <b>{highest_nyha['DEATH_EVENT']:.2f}%</b>, suggesting increased clinical deterioration risk.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# PAGE 3
# =========================
elif page == "🚨 Risk Intelligence":

    st.subheader("🚨 Risk Stratification Intelligence")

    risk_mortality = filtered_df.groupby("risk_category")["DEATH_EVENT"].mean().reset_index()
    risk_mortality["DEATH_EVENT"] *= 100

    fig = px.bar(
        risk_mortality,
        x="risk_category",
        y="DEATH_EVENT",
        color="risk_category",
        title="Mortality Rate by Risk Category",
        labels={"DEATH_EVENT": "Mortality Rate (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    critical_df = filtered_df[filtered_df["risk_category"] == "Critical"]
    low_df = filtered_df[filtered_df["risk_category"] == "Low"]

    critical_mortality = critical_df["DEATH_EVENT"].mean() * 100 if len(critical_df) > 0 else 0
    low_mortality = low_df["DEATH_EVENT"].mean() * 100 if len(low_df) > 0 else 0

    st.markdown("### 🧠 Quantified Risk Insights")

    st.markdown(
        f"""
        <div class="insight-box">
        Critical-risk patients show <b>{critical_mortality:.2f}%</b> mortality compared with 
        <b>{low_mortality:.2f}%</b> among low-risk patients.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="recommend-box">
        <b>Recommendation:</b> Prioritize AI-assisted surveillance for high and critical-risk cohorts. 
        Targeting the top risk groups could focus clinical review on approximately 
        <b>{len(filtered_df[filtered_df['risk_category'].isin(['High','Critical'])]):,}</b> patients.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# PAGE 4
# =========================
elif page == "🏨 Hospital Operations":

    st.subheader("🏨 Hospital Operations Intelligence")

    hospital_mortality = filtered_df.groupby("hospital_site")["DEATH_EVENT"].mean().reset_index()
    hospital_mortality["DEATH_EVENT"] *= 100

    fig = px.bar(
        hospital_mortality,
        x="hospital_site",
        y="DEATH_EVENT",
        color="hospital_site",
        title="Mortality Rate by Hospital Site",
        labels={"DEATH_EVENT": "Mortality Rate (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        filtered_df,
        x="risk_category",
        y="length_of_stay_days",
        color="risk_category",
        title="Length of Stay by Risk Category"
    )
    st.plotly_chart(fig, use_container_width=True)

    highest_site = hospital_mortality.sort_values("DEATH_EVENT", ascending=False).iloc[0]

    st.markdown("### 🧠 Quantified Operational Insights")

    st.markdown(
        f"""
        <div class="insight-box">
        <b>{highest_site['hospital_site']}</b> has the highest observed mortality rate at 
        <b>{highest_site['DEATH_EVENT']:.2f}%</b>, requiring site-level review of escalation pathways.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="recommend-box">
        <b>Operational opportunity:</b> Reducing average LOS by 0.5 days across this cohort could release approximately 
        <b>{int(total_patients * 0.5):,}</b> bed-days.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# PAGE 5
# =========================
elif page == "🧬 Biomarker Intelligence":

    st.subheader("🧬 Biomarker Intelligence")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            filtered_df,
            x="bnp",
            nbins=40,
            title="BNP Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.box(
            filtered_df,
            x="DEATH_EVENT",
            y="bnp",
            color="DEATH_EVENT",
            title="BNP by Mortality Outcome"
        )
        st.plotly_chart(fig, use_container_width=True)

    bnp_survived = filtered_df[filtered_df["DEATH_EVENT"] == 0]["bnp"].median()
    bnp_died = filtered_df[filtered_df["DEATH_EVENT"] == 1]["bnp"].median()

    st.markdown("### 🧠 Quantified Biomarker Insights")

    st.markdown(
        f"""
        <div class="insight-box">
        Median BNP among mortality cases is <b>{bnp_died:.1f}</b> compared with 
        <b>{bnp_survived:.1f}</b> among survivors, suggesting biomarker-driven risk separation.
        </div>
        """,
        unsafe_allow_html=True
    )
elif page == "🚨 High-Risk Patient Explorer":
    render_high_risk_explorer(filtered_df)

elif page == "🧠 Mortality AI Prediction":
    render_prediction_page(filtered_df)

elif page == "🔍 Explainable AI Insights":
    render_explainability_page(filtered_df)

elif page == "🤖 Executive Clinical AI Assistant":
    render_executive_ai_assistant(filtered_df)
# =========================
# PAGE 6
# =========================
elif page == "💡 Executive Recommendations":

    st.subheader("💡 Executive Recommendations")

    readmission_events = int(filtered_df["readmission_30d"].sum())
    possible_10pct_reduction = int(readmission_events * 0.10)
    possible_15pct_reduction = int(readmission_events * 0.15)

    st.markdown(
        f"""
        <div class="recommend-box">
        <b>1. Reduce readmission burden:</b> Current 30-day readmission rate is 
        <b>{readmission_rate:.2f}%</b>, representing <b>{readmission_events:,}</b> events. 
        A 10–15% reduction could prevent approximately 
        <b>{possible_10pct_reduction:,}–{possible_15pct_reduction:,}</b> repeat admissions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="recommend-box">
        <b>2. Optimize bed capacity:</b> Current inpatient utilization is approximately 
        <b>{int(total_bed_days):,}</b> bed-days. Reducing LOS by 0.5 days could release 
        <b>{int(total_patients * 0.5):,}</b> bed-days.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="recommend-box">
        <b>3. Prioritize high-risk surveillance:</b> High and critical-risk patients represent 
        <b>{len(filtered_df[filtered_df['risk_category'].isin(['High','Critical'])]):,}</b> patients. 
        These groups should be prioritized for AI-supported review, escalation planning, and post-discharge follow-up.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="recommend-box">
    <b>4. Deploy biomarker-driven triage:</b>
    BNP, eGFR, serum sodium, troponin, and systolic BP should be incorporated into mortality surveillance workflows because these biomarkers consistently emerged as high-impact mortality predictors within the explainable AI model.
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="executive-footer">', unsafe_allow_html=True)

st.markdown(
    "<b>🫀 CardioIntel AI · Executive Cardiovascular Intelligence Platform</b>",
    unsafe_allow_html=True
)

st.markdown(
    "Clinical AI • Predictive Analytics • Explainable AI • Operational Intelligence"
)

st.markdown(
    """
    <span style="
        display:inline-block;
        padding:10px 20px;
        border-radius:999px;
        background:linear-gradient(90deg,#0ea5e9,#22c55e);
        color:white;
        font-size:12px;
        font-weight:800;
        letter-spacing:0.5px;">
        BUILT BY DR SAMUEL ISRAEL | HEALTHCARE AI & DIGITAL TRANSFORMATION SPECIALIST
    </span>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)