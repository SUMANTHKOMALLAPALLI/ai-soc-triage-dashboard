import streamlit as st
import pandas as pd
import numpy as np
import json
from openai import OpenAI

st.set_page_config(
    page_title="SOC Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Assisted SOC Intelligence Dashboard")

st.caption(
    "Prototype 2 | Synthetic security data | Predictive security intelligence"
)

# -------------------------------------------------
# Load historical security data
# -------------------------------------------------

df = pd.read_csv("security_history.csv")
df["date"] = pd.to_datetime(df["date"])

# Combine all applications by day
daily = df.groupby("date")[
    [
        "phishing_incidents",
        "risky_signins",
        "malware_incidents",
        "powershell_incidents"
    ]
].sum()

recent = daily.tail(30)

incident_types = {
    "Phishing": "phishing_incidents",
    "Risky Sign-In": "risky_signins",
    "Malware": "malware_incidents",
    "Suspicious PowerShell": "powershell_incidents"
}

forecast_results = {}

# -------------------------------------------------
# Forecast next 7 days
# -------------------------------------------------

for name, column in incident_types.items():

    values = recent[column].values

    x = np.arange(len(values))

    slope, intercept = np.polyfit(x, values, 1)

    future_x = np.arange(
        len(values),
        len(values) + 7
    )

    predictions = slope * future_x + intercept

    predictions = np.maximum(predictions, 0)

    predicted_total = round(predictions.sum())

    current_week = recent[column].tail(7).sum()

    change = predicted_total - current_week

    if change > 2:
        trend = "Increasing"
    elif change < -2:
        trend = "Decreasing"
    else:
        trend = "Stable"

    forecast_results[name] = {
        "current": current_week,
        "predicted": predicted_total,
        "trend": trend
    }

# -------------------------------------------------
# Forecast Cards
# -------------------------------------------------

st.subheader("🔮 Incident Forecast — Next 7 Days")

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("Phishing", col1),
    ("Risky Sign-In", col2),
    ("Malware", col3),
    ("Suspicious PowerShell", col4)
]

for incident, column in cards:

    result = forecast_results[incident]

    with column:
        st.metric(
            label=incident,
            value=result["predicted"],
            delta=result["predicted"] - result["current"]
        )

        st.write("Trend:", result["trend"])

st.divider()

# -------------------------------------------------
# Intelligence Message
# -------------------------------------------------

st.subheader("🧠 Security Intelligence")

increasing = [
    name
    for name, result in forecast_results.items()
    if result["trend"] == "Increasing"
]

if increasing:
    st.warning(
       "Trend analysis identified increasing activity for: "
        + ", ".join(increasing)
    )
else:
    st.success(
        "No major incident increase is currently predicted."
    )

st.divider()

# -------------------------------------------------
# Historical Trend Chart
# -------------------------------------------------

st.subheader("📈 Recent Incident Trends")

chart_data = recent.rename(
    columns={
        "phishing_incidents": "Phishing",
        "risky_signins": "Risky Sign-In",
        "malware_incidents": "Malware",
        "powershell_incidents": "Suspicious PowerShell"
    }
)

st.line_chart(chart_data)

st.info(
    "The forecast uses the most recent 30 days of synthetic security history "
    "to estimate incident volume for the next 7 days."
)
# -------------------------------------------------
# Traffic Intelligence
# -------------------------------------------------

st.divider()
st.subheader("🌐 Traffic Intelligence")

# Use older data as normal baseline
cutoff_date = df["date"].max() - pd.Timedelta(days=7)

baseline = df[df["date"] < cutoff_date]
recent_traffic = df[df["date"] >= cutoff_date].copy()

# Calculate normal traffic behavior for each application
traffic_stats = baseline.groupby("application").agg(
    avg_outbound=("outbound_mb", "mean"),
    std_outbound=("outbound_mb", "std"),
    avg_connections=("unusual_connections", "mean"),
    std_connections=("unusual_connections", "std")
)

# Avoid divide-by-zero
traffic_stats["std_outbound"] = traffic_stats["std_outbound"].replace(0, 1)
traffic_stats["std_connections"] = traffic_stats["std_connections"].replace(0, 1)

recent_traffic = recent_traffic.merge(
    traffic_stats,
    on="application",
    how="left"
)

# Compare recent activity with normal behavior
recent_traffic["traffic_zscore"] = (
    (recent_traffic["outbound_mb"] - recent_traffic["avg_outbound"])
    / recent_traffic["std_outbound"]
)

recent_traffic["connection_zscore"] = (
    (recent_traffic["unusual_connections"] - recent_traffic["avg_connections"])
    / recent_traffic["std_connections"]
)

recent_traffic["traffic_anomaly"] = (
    (recent_traffic["traffic_zscore"] > 2)
    | (recent_traffic["connection_zscore"] > 2)
)

traffic_anomalies = recent_traffic[
    recent_traffic["traffic_anomaly"]
].copy()

# Create anomaly score
traffic_anomalies["anomaly_score"] = (
    traffic_anomalies["traffic_zscore"].clip(lower=0) * 10
    + traffic_anomalies["connection_zscore"].clip(lower=0) * 10
)

traffic_anomalies["anomaly_score"] = (
    traffic_anomalies["anomaly_score"]
    .round()
    .clip(upper=100)
)

traffic_anomalies = traffic_anomalies.sort_values(
    "anomaly_score",
    ascending=False
)

# Dashboard summary
col1, col2, col3 = st.columns(3)

col1.metric(
    "Traffic Anomalies",
    len(traffic_anomalies)
)

if not traffic_anomalies.empty:

    highest = traffic_anomalies.iloc[0]

    col2.metric(
        "Highest Anomaly Score",
        f"{int(highest['anomaly_score'])}/100"
    )

    col3.metric(
        "Most Concerning App",
        highest["application"]
    )

    st.error(
        f"Unusual activity detected for {highest['application']}. "
        f"Outbound traffic reached {int(highest['outbound_mb'])} MB "
        f"with {int(highest['unusual_connections'])} unusual connections."
    )

    display_anomalies = traffic_anomalies[
        [
            "date",
            "application",
            "outbound_mb",
            "unusual_connections",
            "anomaly_score"
        ]
    ].head(10).copy()

    display_anomalies.columns = [
        "Date",
        "Application",
        "Outbound Traffic (MB)",
        "Unusual Connections",
        "Anomaly Score"
    ]

    st.dataframe(
        display_anomalies,
        width="stretch",
        hide_index=True
    )

else:
    st.success("No major unusual network traffic detected.")

st.info(
    "Traffic Intelligence compares recent activity with each application's "
    "historical baseline. Activity significantly above normal is flagged "
    "for analyst review."
)
# -------------------------------------------------
# At-Risk Application Prediction
# -------------------------------------------------

st.divider()
st.subheader("⚠️ At-Risk Application Prediction")

application_results = []

for app in df["application"].unique():

    app_data = (
        df[df["application"] == app]
        .sort_values("date")
        .tail(30)
    )

    values = app_data["risk_score"].values

    x = np.arange(len(values))

    # Predict future risk using recent trend
    slope, intercept = np.polyfit(x, values, 1)

    future_x = np.arange(
        len(values),
        len(values) + 7
    )

    future_predictions = slope * future_x + intercept

    future_predictions = np.clip(
        future_predictions,
        0,
        100
    )

    predicted_risk = round(
        future_predictions.mean()
    )

    current_risk = round(
        app_data["risk_score"].tail(7).mean()
    )

    difference = predicted_risk - current_risk

    if difference >= 3:
        trend = "Increasing"
    elif difference <= -3:
        trend = "Decreasing"
    else:
        trend = "Stable"

    recent_app = app_data.tail(7)

    # Identify main risk reason
    risk_drivers = {
        "Phishing Activity":
            recent_app["phishing_incidents"].sum() * 4,

        "Risky Sign-Ins":
            recent_app["risky_signins"].sum() * 5,

        "Malware Activity":
            recent_app["malware_incidents"].sum() * 10,

        "Suspicious PowerShell":
            recent_app["powershell_incidents"].sum() * 8,

        "Failed Logins":
            recent_app["failed_logins"].sum() * 0.5,

        "Unusual Connections":
            recent_app["unusual_connections"].sum() * 3
    }

    top_driver = max(
        risk_drivers,
        key=risk_drivers.get
    )

    application_results.append({
        "Application": app,
        "Current Risk": current_risk,
        "Predicted Risk": predicted_risk,
        "Trend": trend,
        "Main Risk Driver": top_driver
    })

risk_df = pd.DataFrame(application_results)

risk_df = risk_df.sort_values(
    "Predicted Risk",
    ascending=False
)

# Highest-risk application
highest_app = risk_df.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Highest-Risk Application",
    highest_app["Application"]
)

col2.metric(
    "Predicted Risk Score",
    f"{highest_app['Predicted Risk']}/100"
)

col3.metric(
    "Risk Trend",
    highest_app["Trend"]
)

if highest_app["Predicted Risk"] >= 70:

    st.error(
        f"{highest_app['Application']} is predicted to be at high risk. "
        f"The main risk driver is {highest_app['Main Risk Driver']}."
    )

elif highest_app["Predicted Risk"] >= 40:

    st.warning(
        f"{highest_app['Application']} is predicted to have moderate risk. "
        f"The main risk driver is {highest_app['Main Risk Driver']}."
    )

else:

    st.success(
        "No application is currently predicted to have high risk."
    )

st.dataframe(
    risk_df,
    width="stretch",
    hide_index=True
)

st.info(
    "Application risk prediction uses the recent 30-day security trend "
    "to estimate the expected risk level for the next 7 days."
)
# ============================================================
# Prototype 3 - SOC Alert Upload and Parsing
# ============================================================

st.divider()
st.header("🔎 AI-Assisted SOC Alert Triage")

st.caption(
    "Upload a security alert in JSON format. "
    "The dashboard will automatically extract important investigation details."
)

uploaded_alert = st.file_uploader(
    "Upload Security Alert",
    type=["json"],
    key="soc_alert_upload"
)

if uploaded_alert is not None:
    try:
        alert = json.load(uploaded_alert)

        st.success("Alert uploaded successfully.")

        st.subheader("Alert Overview")

        alert_name = alert.get("alert_name", "Unknown")
        severity = alert.get("severity", "Unknown")
        timestamp = alert.get("timestamp", "Unknown")
        host = alert.get("host", "Unknown")
        user = alert.get("user", "Unknown")
        source_ip = alert.get("source_ip", "Unknown")
        destination_ip = alert.get("destination_ip", "Unknown")
        process = alert.get("process", "Unknown")
        command_line = alert.get("command_line", "Unknown")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Alert", alert_name)
            st.metric("Severity", severity)

        with col2:
            st.metric("Host", host)
            st.metric("User", user)

        with col3:
            st.metric("Source IP", source_ip)
            st.metric("Destination IP", destination_ip)

        st.subheader("Investigation Evidence")

        st.write("**Timestamp:**", timestamp)
        st.write("**Process:**", process)
        st.write("**Command Line:**", command_line)
                # ----------------------------------------------------
        # Automatic SOC Triage
        # ----------------------------------------------------

        st.subheader("Automated SOC Triage")

        risk_score = 0
        indicators = []

        severity_lower = str(severity).lower()
        process_lower = str(process).lower()
        command_lower = str(command_line).lower()

        # Severity scoring
        if severity_lower == "critical":
            risk_score += 50
            indicators.append("Critical severity alert")

        elif severity_lower == "high":
            risk_score += 40
            indicators.append("High severity alert")

        elif severity_lower == "medium":
            risk_score += 20

        elif severity_lower == "low":
            risk_score += 10

        # Process checks
        if "powershell" in process_lower:
            risk_score += 15
            indicators.append("PowerShell execution detected")

        # Command-line checks
        if "executionpolicy bypass" in command_lower:
            risk_score += 15
            indicators.append("PowerShell ExecutionPolicy Bypass detected")

        if "encodedcommand" in command_lower:
            risk_score += 20
            indicators.append("Encoded PowerShell command detected")

        risk_score = min(risk_score, 100)

        # Risk classification
        if risk_score >= 80:
            risk_level = "Critical"
        elif risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Calculated Risk Score", f"{risk_score}/100")

        with col2:
            st.metric("Triage Priority", risk_level)

        st.write("### Suspicious Indicators")

        if indicators:
            for indicator in indicators:
                st.write(f"• {indicator}")
        else:
            st.write("No major suspicious indicators identified.")

        st.write("### Recommended Investigation Steps")

        investigation_steps = [
            "Review the full PowerShell command line.",
            "Check the parent and child processes.",
            "Validate whether the user expected this activity.",
            "Review recent logins for the user account.",
            "Check the destination IP or domain reputation.",
            "Review related EDR and SIEM alerts on the host."
        ]

        for number, step in enumerate(investigation_steps, 1):
            st.write(f"{number}. {step}")

        st.write("### Analyst Decision")

        analyst_decision = st.radio(
            "Choose the analyst decision:",
            ["Pending Review", "Benign", "Suspicious", "Escalate"],
            key="analyst_decision"
        )

        st.info(
            f"Current analyst decision: {analyst_decision}"
        )
                # ----------------------------------------------------
        # AI-Assisted SOC Analysis
        # ----------------------------------------------------

        st.subheader("🤖 AI-Assisted SOC Analysis")

        if st.button("Analyze Alert with AI", key="ai_analyze_button"):

            try:
                client = OpenAI(
                    api_key=st.secrets["OPENAI_API_KEY"]
                )

                ai_prompt = f"""
You are assisting a SOC analyst.

Analyze this security alert carefully.

Alert Name: {alert_name}
Severity: {severity}
Host: {host}
User: {user}
Source IP: {source_ip}
Destination IP: {destination_ip}
Process: {process}
Command Line: {command_line}

Rule-Based Risk Score: {risk_score}/100
Triage Priority: {risk_level}

Suspicious Indicators:
{", ".join(indicators)}

Provide the following:

1. Alert Summary
2. Why This Activity Is Suspicious
3. Important Evidence
4. Recommended Investigation Steps
5. Suggested Disposition: Benign, Suspicious, or Escalate
6. Missing Evidence or Limitations

Do not claim that the host is compromised unless the available evidence proves it.

Keep the answer short, clear, and professional for a SOC analyst.
"""

                with st.spinner("AI is analyzing the alert..."):

                    response = client.responses.create(
                        model="gpt-6-luna",
                        input=ai_prompt
                    )

                st.success("AI analysis completed.")

                st.markdown(response.output_text)

            except Exception as e:
                st.error(f"AI analysis failed: {e}")

        with st.expander("View Raw Alert"):
            st.json(alert)

    except Exception as e:
        st.error(f"Unable to read alert: {e}")

# ============================================================
# About Us and Contact Us
# ============================================================

st.divider()

about_tab, contact_tab = st.tabs(["ℹ️ About Us", "📩 Contact Us"])

with about_tab:
    st.header("About Us")

    st.write("""
    The AI-Assisted SOC Intelligence Dashboard is a cybersecurity
    capstone project developed by Sumanth Komallapalli.

    The goal of this project is to help SOC analysts quickly identify
    important security activity, understand risk, and prioritize
    investigations.

    The dashboard currently provides:

    • Security incident forecasting  
    • Traffic anomaly detection  
    • At-risk application prediction  
    • Security alert upload and parsing  
    • Automated SOC risk scoring  
    • AI-assisted alert analysis  
    • Recommended investigation steps  
    • Analyst decision support

    The current project uses synthetic security data for demonstration
    and testing. The long-term goal is to integrate the dashboard with
    real SIEM, EDR, threat intelligence, and cloud-security platforms.

    The system is designed to assist security analysts, not replace them.
    The analyst remains responsible for the final security decision.
    """)

    st.info(
        "Capstone Project | MS Information Technology | "
        "AI-Assisted SOC Intelligence Dashboard"
    )


with contact_tab:
    st.header("Contact Us")

    st.write("""
    Thank you for your interest in the AI-Assisted SOC Intelligence Dashboard.

    For questions, feedback, collaboration, or information about this project,
    please contact the project developer.
    """)

    st.write("**Developer:** Sumanth Komallapalli")
    st.write("**Project:** AI-Assisted SOC Intelligence Dashboard")
    st.write("**Program:** MS Information Technology")

    st.write("**Email:** sumanthpani16@gmail.com")

    st.link_button(
        "GitHub Repository",
        "https://github.com/SUMANTHKOMALLAPALLI/ai-soc-triage-dashboard"
    )
