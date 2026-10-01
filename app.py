import streamlit as st
import pandas as pd
import numpy as np

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
        "The model identified increasing activity for: "
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

    if difference > 5:
        trend = "Increasing Risk"
    elif difference < -5:
        trend = "Decreasing Risk"
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