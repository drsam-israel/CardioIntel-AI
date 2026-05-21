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

def render_executive_ai_assistant(df):

    st.subheader("🤖 Executive Clinical AI Assistant")
    st.caption(
        "AI-style executive assistant for interpreting cardiovascular risk, operations, biomarkers, and strategic recommendations."
    )

    st.markdown("---")

    mortality_rate = df["DEATH_EVENT"].mean() * 100
    readmission_rate = df["readmission_30d"].mean() * 100
    icu_rate = df["icu_admission"].mean() * 100
    avg_los = df["length_of_stay_days"].mean()
    total_bed_days = df["length_of_stay_days"].sum()

    high_risk_count = len(df[df["risk_category"].isin(["High", "Critical"])])
    readmission_events = int(df["readmission_30d"].sum())

    hospital_mortality = (
        df.groupby("hospital_site")["DEATH_EVENT"]
        .mean()
        .sort_values(ascending=False) * 100
    )

    highest_hospital = hospital_mortality.index[0]
    highest_hospital_rate = hospital_mortality.iloc[0]

    st.markdown("### Ask an Executive Healthcare AI Question")

    question = st.selectbox(
        "Select a question",
        [
            "What is the overall cardiovascular risk profile?",
            "Which hospital has the highest mortality burden?",
            "How significant is the readmission burden?",
            "What are the top biomarker priorities?",
            "What executive actions should leadership take?",
            "How can operational efficiency be improved?"
        ]
    )

    st.markdown("### 🧠 AI Assistant Response")

    if question == "What is the overall cardiovascular risk profile?":
        st.info(
            f"""
            The current filtered cohort contains **{len(df):,} patients** with a mortality burden of 
            **{mortality_rate:.2f}%**, ICU admission rate of **{icu_rate:.2f}%**, and average LOS of 
            **{avg_los:.2f} days**.  

            High and critical-risk patients account for **{high_risk_count:,} patients**, representing the key cohort for
            AI-assisted surveillance and escalation planning.
            """
        )

    elif question == "Which hospital has the highest mortality burden?":
        st.warning(
            f"""
            **{highest_hospital}** has the highest observed mortality rate at **{highest_hospital_rate:.2f}%**.  

            This site should be prioritized for review of escalation pathways, discharge planning, cardiovascular care
            coordination, and high-risk patient monitoring workflows.
            """
        )

    elif question == "How significant is the readmission burden?":
        avoid_10 = int(readmission_events * 0.10)
        avoid_15 = int(readmission_events * 0.15)

        st.info(
            f"""
            The 30-day readmission rate is **{readmission_rate:.2f}%**, representing approximately 
            **{readmission_events:,} repeat admissions**.  

            A targeted 10–15% reduction strategy could prevent approximately **{avoid_10:,}–{avoid_15:,}**
            repeat admissions.
            """
        )

    elif question == "What are the top biomarker priorities?":
        st.success(
            """
            The strongest clinical surveillance priorities are:

            - **BNP** for ventricular stress and decompensation risk  
            - **eGFR / serum creatinine** for cardio-renal deterioration  
            - **serum sodium** for electrolyte instability and advanced HF risk  
            - **troponin-I** for myocardial injury  
            - **systolic BP and SpO2** for hemodynamic and oxygenation status
            """
        )

    elif question == "What executive actions should leadership take?":
        st.success(
            f"""
            Recommended leadership actions:

            1. Prioritize surveillance for **{high_risk_count:,} high/critical-risk patients**.  
            2. Implement readmission reduction pathways targeting **{readmission_rate:.2f}%** readmission burden.  
            3. Deploy biomarker-triggered escalation protocols using BNP, eGFR, sodium, troponin, and BP.  
            4. Benchmark high-mortality hospital sites for operational improvement.  
            5. Integrate explainable AI outputs into clinical review workflows.
            """
        )

    elif question == "How can operational efficiency be improved?":
        released_bed_days = int(len(df) * 0.5)

        st.info(
            f"""
            Current inpatient utilization is approximately **{int(total_bed_days):,} bed-days**.  

            Reducing average LOS by just **0.5 days** across the cohort could release approximately 
            **{released_bed_days:,} bed-days**, improving bed capacity, throughput, and operational resilience.
            """
        )