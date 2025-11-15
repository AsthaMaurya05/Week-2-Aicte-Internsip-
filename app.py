# app.py
import streamlit as st
import pandas as pd
import os
import plotly.graph_objs as go

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI-Powered Carbon Emission Forecast Dashboard",
    layout="wide",
    page_icon="🌍"
)

# ---------- LOAD DATA ----------
st.title("🌍 AI-Powered Carbon Emission Forecast Dashboard")

st.markdown("""
### 🔋 India’s Electricity Generation & Carbon Emission Forecast (1985–2035)

This dashboard presents:
- Forecasted **electricity generation** for all major energy sources  
- Predicted **carbon emissions**  
- Interactive tools to explore future scenarios  
""")

data_path = "result/total_emission_forecast.csv"
if not os.path.exists(data_path):
    st.error("⚠️ total_emission_forecast.csv is missing. Please run emission_calculator.py")
    st.stop()

df = pd.read_csv(data_path)
sources = ['bioenergy', 'solar', 'wind', 'hydro', 'nuclear', 'oil', 'gas', 'coal']

# ============================================================
# 🎯 SUMMARY KPI CARDS (Feature #5)
# ============================================================
st.markdown("## 📊 Key Insights (2035 Projection)")

col1, col2, col3, col4 = st.columns(4)

latest_year = df["year"].iloc[-1]
latest_emission = df["total_emission_MtCO2"].iloc[-1]

total_energy_2035 = df[sources].iloc[-1].sum()
renewables_2035 = df[["solar", "wind", "hydro", "bioenergy"]].iloc[-1].sum()
renewable_share = (renewables_2035 / total_energy_2035) * 100

coal_2035 = df["coal"].iloc[-1]

with col1:
    st.metric("🔋 Total Electricity (2035)", f"{total_energy_2035:.1f} TWh")

with col2:
    st.metric("🌱 Renewable Share (2035)", f"{renewable_share:.1f}%")

with col3:
    st.metric("🏭 Carbon Emissions (2035)", f"{latest_emission:.1f} MtCO₂")

with col4:
    st.metric("🔥 Coal Generation (2035)", f"{coal_2035:.1f} TWh")

st.markdown("---")

# ============================================================
# ⚡ ENERGY SOURCE CARDS (Feature #2)
# ============================================================
st.markdown("## 🔌 Energy Source Overview")

info = {
    "Coal": "High CO₂ emissions, dominant in India’s power sector.",
    "Oil": "Small share, declining due to cleaner alternatives.",
    "Gas": "Moderate emissions, often used for peak demand.",
    "Solar": "Fastest growing renewable, zero emissions.",
    "Wind": "Strong renewable contributor, zero emissions.",
    "Hydro": "Stable renewable source with low emissions.",
    "Nuclear": "Low CO₂, high stability, long-term investment.",
    "Bioenergy": "Low carbon alternative using biomass & organic waste."
}

cols = st.columns(4)
i = 0
for fuel, desc in info.items():
    with cols[i % 4]:
        st.markdown(f"""
        <div style="padding:10px; border-radius:8px; background-color:#f2f2f2;">
            <h4>{fuel}</h4>
            <p style="font-size:14px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    i += 1

st.markdown("---")

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
st.sidebar.header("📌 Navigation")
view_option = st.sidebar.radio(
    "Choose a section:",
    ["Energy Forecast", "Carbon Emission Trend", "What-if Simulator"]
)

# ============================================================
# 1️⃣ ENERGY FORECAST (Plotly Interactive) — Feature #1
# ============================================================
if view_option == "Energy Forecast":
    st.subheader("📊 Electricity Generation Forecast (Interactive Plotly)")

    st.markdown("""
    This section shows forecasted **electricity generation** from selected sources using 
    **interactive Plotly charts** and a detailed **forecast table** with insights.
    """)

    # ---------------- SELECT SOURCES ----------------
    selected_sources = st.multiselect(
        "Select Energy Sources:",
        sources,
        default=["coal", "solar", "wind"]
    )

    # ---------------- INTERACTIVE PLOTLY CHART ----------------
    fig = go.Figure()

    for s in selected_sources:
        fig.add_trace(go.Scatter(
            x=df["year"],
            y=df[s],
            mode="lines+markers",
            name=s.capitalize(),
            line=dict(width=3)
        ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Generation (TWh)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # 📋 BEAUTIFUL + INTERACTIVE FORECAST TABLE
    # ============================================================

    st.markdown("### 📋 Electricity Generation Forecast Table (TWh)")
    st.markdown("""
    The table below displays the **forecasted values** for each selected source.  
    This helps users compare how much each energy type contributes to India's electricity mix.
    """)

    # Create final table
    table_df = df[["year"] + selected_sources].tail(12)

    # Capitalize column names (Coal, Solar…)
    friendly = {s: s.capitalize() for s in selected_sources}
    table_df = table_df.rename(columns=friendly)

    # Interactive table with gradient styling
    st.dataframe(
        table_df.style.background_gradient(cmap="YlGnBu"),
        use_container_width=True
    )

    # Table caption
    st.caption("""
    📘 **How to read this table:**  
    - **Year:** The forecast year  
    - **Coal, Solar, Wind, etc.:** Electricity generated in **Terawatt-hours (TWh)**  
    - Higher numbers indicate greater energy production  
    """)

    # ============================================================
    # 🔍 KEY OBSERVATIONS (AUTO-GENERATED)
    # ============================================================

    st.markdown("## 🔍 Key Observations")

    for s in selected_sources:
        start = df[s].iloc[-12]
        end = df[s].iloc[-1]

        if start == 0:
            change = 0
        else:
            change = ((end - start) / start) * 100

        trend = "📈 Increasing" if change > 0 else "📉 Decreasing" if change < 0 else "➖ Stable"

        st.markdown(f"""
        <div style="background-color:#eaf4ff; padding:12px; border-radius:8px; margin-bottom:10px;">
            <b>{s.capitalize()}</b> → {trend}, approximately 
            <b>{change:.2f}% change</b> over the last decade of forecasts.
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 2️⃣ CARBON EMISSION TREND (Plotly)
# ============================================================
elif view_option == "Carbon Emission Trend":
    st.subheader("🌍 Total Carbon Emission Forecast (MtCO₂)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["total_emission_MtCO2"],
        mode="lines+markers",
        line=dict(color="red", width=4),
        name="Total Emissions"
    ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="MtCO₂",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Recent Emission Data")
    st.dataframe(df[["year", "total_emission_MtCO2"]].tail(12))

# ============================================================
# 3️⃣ WHAT-IF SIMULATOR
# ============================================================
else:
    st.subheader("🔧 What-if Scenario Simulator")

    st.markdown("""
    Adjust **Solar/Wind increase** and **Coal reduction** to estimate changes in India's CO₂ emissions.
    """)

    col1, col2, col3 = st.columns(3)
    solar_boost = col1.slider("Increase Solar (%)", 0, 100, 10)
    wind_boost = col2.slider("Increase Wind (%)", 0, 100, 10)
    coal_reduction = col3.slider("Reduce Coal (%)", 0, 100, 20)

    scenario = df.copy()
    scenario["new_emission"] = df["total_emission_MtCO2"] * (
        1 - solar_boost/300 - wind_boost/300 - coal_reduction/150
    )

    reduction = (1 - scenario["new_emission"].mean() / df["total_emission_MtCO2"].mean()) * 100

    st.metric("🌱 Projected CO₂ Reduction", f"{reduction:.2f}%")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["year"], y=df["total_emission_MtCO2"],
                             mode="lines", name="Current"))
    fig.add_trace(go.Scatter(x=df["year"], y=scenario["new_emission"],
                             mode="lines", name="Simulated"))
    fig.update_layout(template="plotly_white", height=500)

    st.plotly_chart(fig, use_container_width=True)
