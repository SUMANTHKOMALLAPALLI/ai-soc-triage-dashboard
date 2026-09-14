import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI-Assisted SOC Triage Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Sample SOC Alerts
# -----------------------------
alerts = [
    {
        "Alert": "Suspicious PowerShell",
        "User": "John Smith",
        "Device": "WIN-1024",
        "IP": "192.168.10.25",
        "Priority": "High",
        "Status": "Open",
        "Evidence": "powershell.exe attempted to download a file from an external domain.",
        "Summary": "Suspicious PowerShell activity was detected. The command attempted to download content from an external source.",
        "Steps": [
            "Review the PowerShell command",
            "Check the destination domain",
            "Review the process tree",
            "Check related user activity"
        ]
    },
    {
        "Alert": "Phishing Email",
        "User": "Sarah Lee",
        "Device": "WIN-2045",
        "IP": "10.10.5.15",
        "Priority": "High",
        "Status": "Open",
        "Evidence": "User received an email containing a suspicious login link.",
        "Summary": "A suspicious email containing a login link was detected and may be attempting to steal user credentials.",
        "Steps": [
            "Review the sender address",
            "Check the URL reputation",
            "Confirm whether the user clicked the link",
            "Review recent sign-in activity"
        ]
    },
    {
        "Alert": "Risky Sign-In",
        "User": "David Miller",
        "Device": "LAPTOP-331",
        "IP": "172.16.25.44",
        "Priority": "Medium",
        "Status": "Under Review",
        "Evidence": "Login was observed from an unusual IP address.",
        "Summary": "The user's account signed in from an IP address that is different from normal activity.",
        "Steps": [
            "Check sign-in location",
            "Review MFA activity",
            "Compare with previous user logins",
            "Contact the user if required"
        ]
    },
    {
        "Alert": "Malware Detection",
        "User": "Robert King",
        "Device": "WIN-5011",
        "IP": "10.20.15.18",
        "Priority": "High",
        "Status": "Open",
        "Evidence": "Endpoint protection detected a suspicious executable file.",
        "Summary": "A suspicious executable was detected on the endpoint and may require further investigation.",
        "Steps": [
            "Check file reputation",
            "Review file hash",
            "Check process activity",
            "Consider isolating the device"
        ]
    },
    {
        "Alert": "Unusual Login Location",
        "User": "Emily Davis",
        "Device": "LAPTOP-908",
        "IP": "192.168.50.20",
        "Priority": "Low",
        "Status": "Open",
        "Evidence": "Successful login was recorded from a new geographic location.",
        "Summary": "The user signed in from a location not commonly seen in previous login activity.",
        "Steps": [
            "Review login history",
            "Check device information",
            "Confirm travel or VPN usage",
            "Monitor for additional activity"
        ]
    }
]

# -----------------------------
# Header
# -----------------------------
st.title("🛡️ AI-Assisted SOC Triage Dashboard")

st.caption(
    "Prototype 1 | Sample security data | Human analyst makes the final decision"
)

# -----------------------------
# Dashboard Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Alerts", len(alerts))
col2.metric("High Priority", 3)
col3.metric("Medium Priority", 1)
col4.metric("Low Priority", 1)

st.divider()

# -----------------------------
# Alert Table
# -----------------------------
st.subheader("🚨 Security Alerts")

df = pd.DataFrame(alerts)

st.dataframe(
    df[["Alert", "User", "Priority", "Status"]],
    width="stretch",
    hide_index=True
)

st.divider()

# -----------------------------
# Select Alert
# -----------------------------
st.subheader("🔎 Investigate Alert")

selected_alert = st.selectbox(
    "Select an alert:",
    [alert["Alert"] for alert in alerts]
)

alert = next(
    item for item in alerts
    if item["Alert"] == selected_alert
)

# -----------------------------
# Alert Information
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.write("### Alert Details")
    st.write("**Alert:**", alert["Alert"])
    st.write("**User:**", alert["User"])
    st.write("**Device:**", alert["Device"])
    st.write("**IP Address:**", alert["IP"])
    st.write("**Status:**", alert["Status"])

with col2:
    st.write("### Risk Priority")

    if alert["Priority"] == "High":
        st.error("🔴 HIGH PRIORITY")
    elif alert["Priority"] == "Medium":
        st.warning("🟠 MEDIUM PRIORITY")
    else:
        st.success("🟢 LOW PRIORITY")

st.divider()

# -----------------------------
# Evidence
# -----------------------------
st.subheader("📋 Evidence")

st.write(alert["Evidence"])

# -----------------------------
# AI Summary
# -----------------------------
st.subheader("🤖 AI Alert Summary")

st.info(alert["Summary"])

# -----------------------------
# Investigation Steps
# -----------------------------
st.subheader("🔍 Recommended Investigation Steps")

for number, step in enumerate(alert["Steps"], start=1):
    st.write(f"{number}. {step}")

st.divider()

# -----------------------------
# Analyst Decision
# -----------------------------
st.subheader("👤 Analyst Decision")

st.write(
    "AI provides recommendations, but the security analyst makes the final decision."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("✅ Close as Benign"):
        st.success("Decision recorded: Close as Benign")

with col2:
    if st.button("👀 Monitor"):
        st.info("Decision recorded: Monitor")

with col3:
    if st.button("📞 Validate User"):
        st.warning("Decision recorded: Validate with User")

with col4:
    if st.button("🚨 Escalate"):
        st.error("Decision recorded: Escalate to Incident Response")