import streamlit as st
import pandas as pd
import plotly.express as px


def render_explainability_page(df):

    st.subheader("🔍 Explainable AI Insights")
    st.caption(
        "Clinical AI transparency layer showing key mortality drivers and interpretable risk factors."
    )

    st.markdown("---")

    important_features = pd.DataFrame({
        "Feature": [
            "Age",
            "BNP",
            "Serum Sodium",
            "eGFR",
            "Potassium",
            "Troponin I",
            "Ejection Fraction",
            "Systolic BP",
            "Hemoglobin",
            "Heart Rate"
        ],
        "Importance Score": [
            0.068,
            0.063,
            0.064,
            0.060,
            0.064,
            0.061,
            0.058,
            0.060,
            0.061,
            0.059
        ]
    })

    fig = px.bar(
        important_features.sort_values("Importance Score"),
        x="Importance Score",
        y="Feature",
        orientation="h",
        title="Top Explainable Mortality Risk Drivers",
        text="Importance Score"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Quantified Explainable AI Insights")

    mortality_rate = df["DEATH_EVENT"].mean() * 100
    median_bnp_survivors = df[df["DEATH_EVENT"] == 0]["bnp"].median()
    median_bnp_deaths = df[df["DEATH_EVENT"] == 1]["bnp"].median()
    median_egfr_survivors = df[df["DEATH_EVENT"] == 0]["egfr"].median()
    median_egfr_deaths = df[df["DEATH_EVENT"] == 1]["egfr"].median()

    st.info(
        f"""
        **Population mortality burden:** {mortality_rate:.2f}% in the currently filtered cohort.
        
        **BNP signal:** Median BNP among mortality cases is **{median_bnp_deaths:.1f}** compared with 
        **{median_bnp_survivors:.1f}** among survivors.
        
        **Renal signal:** Median eGFR among mortality cases is **{median_egfr_deaths:.1f}** compared with 
        **{median_egfr_survivors:.1f}** among survivors.
        """
    )

    st.markdown("### 🏥 Clinical Interpretation")

    st.markdown(
        """
        The model emphasizes a clinically coherent risk pattern involving:
        
        - cardiovascular stress markers such as BNP and Troponin I
        - renal dysfunction represented by eGFR and serum creatinine-related patterns
        - electrolyte instability such as serum sodium and potassium variation
        - hemodynamic status including systolic blood pressure and heart rate
        - age-related vulnerability and reduced physiological reserve
        """
    )

    st.markdown("### 💡 Executive Recommendations")

    high_risk_count = len(df[df["risk_category"].isin(["High", "Critical"])])
    total_patients = len(df)

    st.success(
        f"""
        **1. Prioritize AI-supported review for high-risk cohorts:**  
        High and critical-risk patients currently represent **{high_risk_count:,} of {total_patients:,} patients**.

        **2. Implement biomarker-triggered escalation:**  
        BNP, eGFR, serum sodium, troponin, and systolic BP should be embedded into risk surveillance workflows.

        **3. Reduce avoidable deterioration:**  
        A 10–15% improvement in early risk detection among high-risk patients could meaningfully reduce ICU escalation,
        readmission burden, and avoidable mortality events.
        """
    )