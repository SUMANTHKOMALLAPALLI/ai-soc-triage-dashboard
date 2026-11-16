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
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #eef4ff 0%,
        #f8fbff 50%,
        #f5f3ff 100%
    );
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Animated banner background */
@keyframes gradientMove {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Fade-in animation */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Pulse animation */
@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 0 0 rgba(34,197,94,0.35);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(34,197,94,0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(34,197,94,0);
    }
}

/* Make navigation buttons animate in */
.nav-button {
    animation: fadeUp 0.7s ease-out;
}

/* Animate Streamlit metric cards */
[data-testid="stMetric"] {
    animation: fadeUp 0.8s ease-out;
}

/* Smooth hover effect */
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    transition: 0.25s ease;
}

/* System status boxes */
div[data-testid="stAlert"] {
    animation: fadeUp 0.8s ease-out;
}

/* Smooth page content */
.block-container {
    animation: fadeUp 0.6s ease-out;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(110deg,#172554,#1d4ed8,#7c3aed,#2563eb);background-size:300% 300%;animation:gradientMove 8s ease infinite;padding:28px 32px;border-radius:18px;margin-bottom:18px;box-shadow:0 10px 30px rgba(37,99,235,0.20);">
<h1 style="color:white;margin:0;font-size:42px;font-weight:800;">🛡️ AI-Assisted SOC Intelligence Dashboard</h1>
<p style="color:#e0e7ff;font-size:17px;margin-top:8px;margin-bottom:0;">Predict • Detect • Triage • Investigate • Decide</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.nav-container {
    display: flex;
    gap: 12px;
    margin: 10px 0 28px 0;
    flex-wrap: wrap;
}

.nav-button {
    text-decoration: none !important;
    padding: 10px 18px;
    border: 1px solid #d9d9d9;
    border-radius: 10px;
    font-weight: 600;
    display: inline-block;
    background: #ffffff;
    color: #202124 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.nav-button:hover {
    border-color: #8aa7c7;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
</style>

<div class="nav-container">
    <a class="nav-button" href="#dashboard">🏠 Dashboard</a>
    <a class="nav-button" href="#alert-triage">🔎 Alert Triage</a>
    <a class="nav-button" href="#about-us">ℹ️ About Us</a>
    <a class="nav-button" href="#contact-us">📩 Contact Us</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)

st.caption(
    "Final Capstone Prototype | Synthetic Security Data | AI-Assisted SOC Analysis"
)
st.markdown("""
<div style="
    margin-top: 20px;
    margin-bottom: 28px;
">

<h2 style="
    color:#1e3a8a;
    margin-bottom:16px;
">
⚙️ How It Works
</h2>

<div style="
    display:flex;
    gap:12px;
    flex-wrap:wrap;
">

<div style="
    flex:1;
    min-width:180px;
    background:white;
    border-radius:14px;
    padding:18px;
    border-top:4px solid #2563eb;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
">
    <b>1. Security Data</b><br>
    <span style="color:#64748b;">
    Historical security data and uploaded alerts
    </span>
</div>

<div style="
    flex:1;
    min-width:180px;
    background:white;
    border-radius:14px;
    padding:18px;
    border-top:4px solid #06b6d4;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
">
    <b>2. Detect</b><br>
    <span style="color:#64748b;">
    Identify trends, anomalies, and suspicious indicators
    </span>
</div>

<div style="
    flex:1;
    min-width:180px;
    background:white;
    border-radius:14px;
    padding:18px;
    border-top:4px solid #8b5cf6;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
">
    <b>3. Triage</b><br>
    <span style="color:#64748b;">
    Calculate risk score and investigation priority
    </span>
</div>

<div style="
    flex:1;
    min-width:180px;
    background:white;
    border-radius:14px;
    padding:18px;
    border-top:4px solid #ec4899;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
">
    <b>4. AI Analysis</b><br>
    <span style="color:#64748b;">
    Generate summary, evidence, and investigation steps
    </span>
</div>

<div style="
    flex:1;
    min-width:180px;
    background:white;
    border-radius:14px;
    padding:18px;
    border-top:4px solid #22c55e;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
">
    <b>5. Analyst Decision</b><br>
    <span style="color:#64748b;">
    Benign, Suspicious, or Escalate
    </span>
</div>

</div>
</div>
""", unsafe_allow_html=True)
st.markdown("## 🟢 System Status")

status1, status2, status3, status4 = st.columns(4)

with status1:
    st.success("Dashboard\n\nOperational")

with status2:
    st.info("AI Analysis\n\nConnected")

with status3:
    st.warning("Data Source\n\nSynthetic")

with status4:
    st.info("SIEM Integration\n\nPlanned")

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
st.markdown('<div id="alert-triage"></div>', unsafe_allow_html=True)
st.header("🔎 AI-Assisted SOC Alert Triage")

st.caption(
    "Upload a security alert in JSON format. "
    "The dashboard will automatically extract important investigation details."
)

demo_alert = {
    "alert_name": "Suspicious PowerShell Execution",
    "severity": "High",
    "timestamp": "2026-11-15T14:30:00",
    "host": "FIN-SRV-01",
    "user": "finance.user",
    "source_ip": "10.10.20.15",
    "destination_ip": "203.0.113.66",
    "process": "powershell.exe",
    "command_line": "powershell.exe -ExecutionPolicy Bypass -EncodedCommand TESTDATA"
}
demo_alert_2 = {
    "alert_name": "Suspicious Privileged Sign-In",
    "severity": "High",
    "timestamp": "2026-11-15T15:10:00",
    "host": "AZURE-PORTAL",
    "user": "finance.admin",
    "source_ip": "198.51.100.45",
    "destination_ip": "10.10.10.20",
    "process": "browser",
    "command_line": "Interactive sign-in from a new location"
}

demo_alert_3 = {
    "alert_name": "Possible Malware Execution",
    "severity": "Critical",
    "timestamp": "2026-11-15T15:25:00",
    "host": "HR-LAPTOP-22",
    "user": "hr.user",
    "source_ip": "10.10.30.25",
    "destination_ip": "203.0.113.80",
    "process": "rundll32.exe",
    "command_line": "rundll32.exe suspicious.dll,Start"
}

demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    use_demo_alert = st.button(
        "⚡ PowerShell Demo",
        key="demo_powershell"
    )

with demo_col2:
    use_demo_alert_2 = st.button(
        "🔐 Sign-In Demo",
        key="demo_signin"
    )

with demo_col3:
    use_demo_alert_3 = st.button(
        "🦠 Malware Demo",
        key="demo_malware"
    )

uploaded_alert = st.file_uploader(
    "Or upload your own Security Alert",
    type=["json"],
    key="soc_alert_upload"
)

if uploaded_alert is not None or use_demo_alert or use_demo_alert_2 or use_demo_alert_3:
    try:

        if use_demo_alert:
            alert = demo_alert
            st.success("PowerShell demo alert loaded successfully.")

        elif use_demo_alert_2:
            alert = demo_alert_2
            st.success("Suspicious sign-in demo alert loaded successfully.")

        elif use_demo_alert_3:
            alert = demo_alert_3
            st.success("Malware demo alert loaded successfully.")

        else:
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

        col1.metric(
            "Calculated Risk Score",
            f"{risk_score}/100"
        )

        col2.metric(
            "Triage Priority",
            risk_level
        )

        risk_reasons = " • ".join(indicators) if indicators else "No major suspicious indicators were identified."

        st.info(
            f"ℹ️ **Why this risk score?**  \n{risk_reasons}  \n\n"
            "This is a rule-based prototype score used to support analyst prioritization. "
            "The analyst still makes the final decision."
        )

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

                ai_prompt = (
                    "You are assisting a SOC analyst.\n\n"
                    "Analyze this security alert carefully.\n\n"
                    f"Alert Name: {alert_name}\n"
                    f"Severity: {severity}\n"
                    f"Host: {host}\n"
                    f"User: {user}\n"
                    f"Source IP: {source_ip}\n"
                    f"Destination IP: {destination_ip}\n"
                    f"Process: {process}\n"
                    f"Command Line: {command_line}\n\n"
                    f"Rule-Based Risk Score: {risk_score}/100\n"
                    f"Triage Priority: {risk_level}\n\n"
                    "Suspicious Indicators:\n"
                    f"{', '.join(indicators)}\n\n"
                    "Provide the following:\n"
                    "1. Alert Summary\n"
                    "2. Why This Activity Is Suspicious\n"
                    "3. Important Evidence\n"
                    "4. Recommended Investigation Steps\n"
                    "5. Suggested Disposition: Benign, Suspicious, or Escalate\n"
                    "6. Missing Evidence or Limitations\n\n"
                    "Do not claim that the host is compromised unless the available evidence proves it.\n"
                    "Keep the answer short, clear, and professional for a SOC analyst."
                )

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

# About Us and Contact Us
# --------------------------------------------

st.divider()

st.markdown("## 🚧 Limitations & Future Work")

col1, col2 = st.columns(2)

with col1:
    st.warning(
        "**Current Limitations**\n\n"
        "- Historical dashboard data is synthetic\n"
        "- Threat intelligence enrichment is not yet connected\n"
        "- Machine-learning anomaly detection is not yet implemented\n"
        "- Live SIEM/EDR API integration is not yet enabled\n"
        "- Current rule-based triage focuses on selected alert indicators"
    )

with col2:
    st.info(
        "**Future Enhancements**\n\n"
        "- Threat intelligence lookups for IPs, domains, and hashes\n"
        "- Machine-learning anomaly detection\n"
        "- Splunk / Microsoft Sentinel integration\n"
        "- CrowdStrike / Defender enrichment\n"
        "- Real-time alert ingestion\n"
        "- Expanded automated investigation workflows"
    )

st.caption(
    "The current application is a working capstone prototype. "
    "These items are planned enhancements for a production-ready version."
)

st.divider()
st.markdown('<div id="about-us"></div>', unsafe_allow_html=True)
st.header("ℹ️ About Us")

st.write(
    "The AI-Assisted SOC Intelligence Dashboard is a cybersecurity "
    "capstone project developed by Sumanth Komallapalli."
)

st.write(
    "The goal of this project is to help SOC analysts quickly identify "
    "important security activity, understand risk, and prioritize investigations."
)

st.markdown(
    "### Current Capabilities\n"
    "- Security incident forecasting\n"
    "- Traffic anomaly detection\n"
    "- At-risk application prediction\n"
    "- Security alert upload and parsing\n"
    "- Automated SOC risk scoring\n"
    "- AI-assisted alert analysis\n"
    "- Recommended investigation steps\n"
    "- Analyst decision support"
)

st.write(
    "The current project uses synthetic security data for demonstration and testing. "
    "The long-term goal is to integrate the dashboard with real SIEM, EDR, "
    "threat intelligence, and cloud-security platforms."
)

st.write(
    "The system is designed to assist security analysts, not replace them. "
    "The analyst remains responsible for the final security decision."
)

st.info(
    "Capstone Project | MS Information Technology | "
    "AI-Assisted SOC Intelligence Dashboard"
)

st.divider()
st.markdown('<div id="contact-us"></div>', unsafe_allow_html=True)

st.header("📩 Contact Us")

st.write(
    "Thank you for your interest in the AI-Assisted SOC Intelligence Dashboard.\n\n"
    "For questions, feedback, collaboration, or information about this project, "
    "please contact the project developer."
)

st.write("**Developer:** Sumanth Komallapalli")
st.write("**Project:** AI-Assisted SOC Intelligence Dashboard")
st.write("**Program:** MS Information Technology")
st.write("**Email:** sumanthpani16@gmail.com")

st.link_button(
    "GitHub Repository",
    "https://github.com/SUMANTHKOMALLAPALLI/ai-soc-triage-dashboard"
)
st.divider()

st.markdown(
    '<div style="text-align:center; color:#64748b; padding:15px;">'
    'AI-Assisted SOC Intelligence Dashboard<br>'
    'Capstone Project | MS Information Technology<br>'
    'Developed by Sumanth Komallapalli'
    '</div>',
    unsafe_allow_html=True
)
