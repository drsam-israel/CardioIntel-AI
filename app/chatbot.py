import streamlit as st
import pandas as pd
import plotly.express as px


def render_high_risk_explorer(df):

    st.subheader("🚨 High-Risk Patient Explorer")
    st.caption(
        "Interactive cohort surveillance tool for identifying high-risk cardiovascular patients requiring prioritized review."
    )

    st.markdown("---")

    high_risk_df = df[df["risk_category"].isin(["High", "Critical"])]

    total_patients = len(df)
    high_risk_count = len(high_risk_df)
    high_risk_percent = (high_risk_count / total_patients) * 100 if total_patients > 0 else 0
    mortality_events = int(high_risk_df["DEATH_EVENT"].sum())
    readmission_events = int(high_risk_df["readmission_30d"].sum())
    icu_events = int(high_risk_df["icu_admission"].sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("High/Critical Patients", f"{high_risk_count:,}")
    c2.metric("High-Risk Share", f"{high_risk_percent:.1f}%")
    c3.metric("Mortality Events", f"{mortality_events:,}")
    c4.metric("Readmission Events", f"{readmission_events:,}")

    st.markdown("### 🏥 High-Risk Cohort Distribution")

    fig = px.histogram(
        high_risk_df,
        x="risk_category",
        color="risk_category",
        title="High & Critical Risk Patient Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏨 High-Risk Patients by Hospital Site")

    hospital_risk = (
        high_risk_df.groupby("hospital_site")
        .size()
        .reset_index(name="High_Risk_Count")
        .sort_values("High_Risk_Count", ascending=False)
    )

    fig = px.bar(
        hospital_risk,
        x="hospital_site",
        y="High_Risk_Count",
        color="hospital_site",
        title="High/Critical-Risk Patient Burden by Hospital"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔎 Patient-Level Risk Table")

    display_cols = [
        "patient_id",
        "hospital_site",
        "care_setting",
        "age",
        "sex_label",
        "nyha_class",
        "hf_phenotype",
        "bnp",
        "egfr",
        "ejection_fraction",
        "risk_category",
        "mortality_risk_score",
        "readmission_30d",
        "icu_admission",
        "DEATH_EVENT"
    ]

    st.dataframe(
        high_risk_df[display_cols].sort_values(
            by="mortality_risk_score",
            ascending=False
        ),
        use_container_width=True,
        height=420
    )

    st.markdown("### 🧠 Quantified Executive Insights")

    st.info(
        f"""
        High and critical-risk patients represent **{high_risk_count:,} of {total_patients:,} patients**
        (**{high_risk_percent:.1f}%** of the filtered cohort).

        Within this high-risk cohort, there are **{mortality_events:,} mortality events**, 
        **{readmission_events:,} readmission events**, and **{icu_events:,} ICU escalation events**.
        """
    )

    st.markdown("### 💡 Strategic Recommendations")

    preventable_readmissions_10 = int(readmission_events * 0.10)
    preventable_readmissions_15 = int(readmission_events * 0.15)

    st.success(
        f"""
        **1. Prioritize high-risk cardiovascular surveillance:**  
        Focus care coordination on the **{high_risk_count:,} high/critical-risk patients**.

        **2. Reduce readmission burden:**  
        A 10–15% reduction in high-risk readmissions could prevent approximately 
        **{preventable_readmissions_10:,}–{preventable_readmissions_15:,} repeat admissions**.

        **3. Improve escalation workflows:**  
        Patients with elevated BNP, reduced eGFR, advanced NYHA class, and prior HF admissions should receive structured follow-up.

        **4. Operational impact:**  
        Earlier identification of this cohort supports ICU demand planning, bed management, and mortality risk reduction initiatives.
        """
    )