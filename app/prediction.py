import streamlit as st
import pandas as pd


def classify_risk(score):
    if score < 30:
        return "Low Risk", "🟢"
    elif score < 55:
        return "Moderate Risk", "🟡"
    elif score < 75:
        return "High Risk", "🟠"
    else:
        return "Critical Risk", "🔴"


def calculate_mortality_risk(
    age, nyha_class, ejection_fraction, bnp, serum_creatinine,
    egfr, serum_sodium, spo2, prior_hf_admissions, troponin_i
):
    score = 0

    score += max(0, (age - 45) * 0.6)
    score += nyha_class * 8
    score += max(0, (40 - ejection_fraction) * 0.8)
    score += min(bnp / 80, 20)
    score += serum_creatinine * 6
    score += max(0, (70 - egfr) * 0.4)
    score += max(0, (136 - serum_sodium) * 2)
    score += max(0, (95 - spo2) * 3)
    score += prior_hf_admissions * 5
    score += troponin_i * 25

    return min(round(score, 1), 100)


def render_prediction_page(df):
    st.subheader("🧠 Mortality AI Prediction Engine")
    st.caption(
        "Interactive clinical decision-support simulator for heart failure mortality risk stratification."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 30, 95, 65)
        nyha_class = st.selectbox("NYHA Class", [1, 2, 3, 4])
        ejection_fraction = st.slider("Ejection Fraction (%)", 10, 75, 38)
        bnp = st.slider("BNP Level", 0, 5000, 450)
        serum_creatinine = st.slider("Serum Creatinine", 0.3, 6.0, 1.2)

    with col2:
        egfr = st.slider("eGFR", 10, 130, 65)
        serum_sodium = st.slider("Serum Sodium", 120, 150, 137)
        spo2 = st.slider("SpO2 (%)", 75, 100, 95)
        prior_hf_admissions = st.slider("Prior HF Admissions", 0, 10, 1)
        troponin_i = st.slider("Troponin I", 0.00, 2.00, 0.05)

    risk_score = calculate_mortality_risk(
        age, nyha_class, ejection_fraction, bnp, serum_creatinine,
        egfr, serum_sodium, spo2, prior_hf_admissions, troponin_i
    )

    risk_label, icon = classify_risk(risk_score)

    st.markdown("## AI Risk Output")

    c1, c2, c3 = st.columns(3)

    c1.metric("Predicted Mortality Risk Score", f"{risk_score}%")
    c2.metric("Risk Category", f"{icon} {risk_label}")
    c3.metric("Recommended Review Priority", "Urgent" if risk_score >= 75 else "Routine/Escalated")

    st.markdown("### 🧠 Quantified Clinical Interpretation")

    if risk_score >= 75:
        st.error(
            f"""
            This patient falls into the **critical-risk category** with an estimated mortality risk score of **{risk_score}%**.  
            Immediate senior clinical review, escalation planning, and intensive monitoring are recommended.
            """
        )
    elif risk_score >= 55:
        st.warning(
            f"""
            This patient falls into the **high-risk category** with an estimated mortality risk score of **{risk_score}%**.  
            Early intervention, medication optimization, and close follow-up are recommended.
            """
        )
    elif risk_score >= 30:
        st.info(
            f"""
            This patient falls into the **moderate-risk category** with an estimated mortality risk score of **{risk_score}%**.  
            Risk-factor optimization and structured follow-up are recommended.
            """
        )
    else:
        st.success(
            f"""
            This patient falls into the **low-risk category** with an estimated mortality risk score of **{risk_score}%**.  
            Continue standard heart failure monitoring and preventive care.
            """
        )

    st.markdown("### 💡 Executive Recommendations")

    st.markdown(
        f"""
        - Patients with **NYHA Class {nyha_class}**, BNP of **{bnp}**, and eGFR of **{egfr}** should be considered for structured risk review.
        - If similar high-risk patients represent just **10% of the cohort**, approximately **{int(len(df) * 0.10):,} patients** may require prioritized surveillance.
        - Reducing high-risk deterioration by **10–15%** could meaningfully lower ICU escalation, readmissions, and avoidable mortality burden.
        """
    )