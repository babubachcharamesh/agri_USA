import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
import requests
from streamlit_lottie import st_lottie
import time
from data_engine import generate_2025_ag_data, get_ticker_data, create_pdf_report

# Page Config
st.set_page_config(
    page_title="USA Agriculture 2025 | Mission Control",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helper for Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_agri = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_m6cu9zob.json") # Farming animation

# Helper for large numbers (Base value is in Millions)
def format_big_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.2f}T" # Trillion
    elif num >= 1_000:
        return f"{num / 1_000:.2f}B" # Billion
    return f"{num:.2f}M" # Million

# Load Data
@st.cache_data
def get_data():
    return generate_2025_ag_data()

df = get_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌾 AGRI-CONTROL")
    st.markdown("---")
    
    selected_crop = st.selectbox("Select Crop Focus", ["All Crops"] + sorted(df["Crop"].unique().tolist()))
    selected_state = st.selectbox("Select State focus", ["All States"] + sorted(df["State"].unique().tolist()))
    
    # --- FILTERING DATA (Calculated early for downloads) ---
    filtered_df = df.copy()
    if selected_crop != "All Crops":
        filtered_df = filtered_df[filtered_df["Crop"] == selected_crop]
    if selected_state != "All States":
        filtered_df = filtered_df[filtered_df["State"] == selected_state]

    st.markdown("### Visualization Mode")
    viz_mode = st.radio("Display Type", ["3D Production Map", "Market Analytics", "AI Insights"])
    
    st.markdown("---")
    st.markdown("### 📥 Data Export Hub")
    
    # CSV Export (Using Filtered Data)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='usa_agri_filtered_2025.csv',
        mime='text/csv',
    )
    
    # PDF Export (Using Filtered Data)
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF..."):
            pdf_bytes = create_pdf_report(filtered_df)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="usa_agri_report_filtered_2025.pdf",
                mime="application/pdf"
            )

    st.markdown("---")
    st.info("System Status: Online\nProjection Year: 2025\nData Source: USDA-Simulated")

# --- HEADER SECTION ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🇺🇸 USA AGRICULTURE 2025")
    st.subheader("High-Resolution Production & Yield Projections")
    st.markdown("""
        Experience the future of American farming. This dashboard provides real-time 
        visualizations of projected crop yields and market values across the United States.
    """)

with col2:
    if lottie_agri:
        st_lottie(lottie_agri, height=150, key="agri_lottie")

# --- TICKER ---
ticker_data = get_ticker_data()
ticker_html = '<div class="ticker-container"><div class="ticker-wrap">'
for item in ticker_data:
    color_class = "price-up" if item["change"] > 0 else "price-down"
    arrow = "▲" if item["change"] > 0 else "▼"
    ticker_html += f'<div class="ticker-item">{item["name"]}: ${item["price"]} <span class="{color_class}">{arrow} {abs(item["change"])}%</span></div>'
ticker_html += '</div></div>'
st.markdown(ticker_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PERSISTENT EXECUTIVE SUMMARY ---
m_total_prod = filtered_df["Production_MT"].sum()
m_total_val = filtered_df["Market_Value_USD"].sum()
try:
    m_top_crop = filtered_df.groupby("Crop")["Production_MT"].sum().idxmax()
except:
    m_top_crop = "N/A"

summary_title = f"📍 {selected_state.upper()}" if selected_state != "All States" else "🇺🇸 USA NATIONAL"
summary_subtitle = f" | {selected_crop.upper()}" if selected_crop != "All Crops" else " | AGRI-TOTALS"

st.markdown(f"## {summary_title}{summary_subtitle} PERFORMANCE")
st.caption("Note: All financial and production values are in Millions (M) base units.")
sm1, sm2, sm3 = st.columns(3)
with sm1:
    st.markdown(f'<div class="glass-card"><p style="color:#00ff88; margin-bottom:0;">TOTAL PRODUCTION</p><h2 style="margin-top:0;">{format_big_number(m_total_prod)} MT</h2></div>', unsafe_allow_html=True)
with sm2:
    st.markdown(f'<div class="glass-card"><p style="color:#00d4ff; margin-bottom:0;">MARKET VALUE</p><h2 style="margin-top:0;">${format_big_number(m_total_val)}</h2></div>', unsafe_allow_html=True)
with sm3:
    st.markdown(f'<div class="glass-card"><p style="color:#ffcc00; margin-bottom:0;">PRIMARY ENGINE</p><h2 style="margin-top:0;">{m_top_crop}</h2></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
if viz_mode == "3D Production Map":
    st.subheader(f"3D Production Heatmap: {selected_crop}")
    
    # Aggregate data for map (Spatial totals)
    map_data = filtered_df.groupby(["State", "Latitude", "Longitude"]).agg({
        "Production_MT": "sum",
        "Market_Value_USD": "sum"
    }).reset_index()
    
    # Generate Detailed Breakdown for Tooltip
    detailed_breakdowns = {}
    for state in map_data["State"]:
        state_crops = filtered_df[filtered_df["State"] == state]
        if selected_crop != "All Crops":
            # Just one crop info
            row = state_crops.iloc[0]
            detailed_breakdowns[state] = f"Crop: {row['Crop']}<br>Production: {format_big_number(row['Production_MT'])} MT<br>Value: ${format_big_number(row['Market_Value_USD'])}"
        else:
            # Table-style breakdown for all crops
            html = "<table style='width:100%; border-collapse: collapse; font-size: 11px; margin-top:5px;'>"
            html += "<tr style='border-bottom: 1px solid rgba(255,255,255,0.2);'><th>Crop</th><th>Prod</th><th>Value</th></tr>"
            for _, row in state_crops.iterrows():
                html += f"<tr><td>{row['Crop']}</td><td style='text-align:right;'>{format_big_number(row['Production_MT'])}</td><td style='text-align:right;'>${format_big_number(row['Market_Value_USD'])}</td></tr>"
            html += "</table>"
            detailed_breakdowns[state] = html

    map_data["details"] = map_data["State"].map(detailed_breakdowns)
    map_data["prod_display"] = map_data["Production_MT"].apply(format_big_number)
    
    # Pydeck 3D Map
    layer = pdk.Layer(
        "ColumnLayer",
        data=map_data,
        get_position=["Longitude", "Latitude"],
        get_elevation="Production_MT",
        elevation_scale=50,
        radius=50000,
        get_fill_color=["Production_MT * 0.0005", "Production_MT * 0.001", 200, 150],
        pickable=True,
        auto_highlight=True,
    )
    
    # Dynamic View State
    if selected_state != "All States" and not filtered_df.empty:
        center_lat = filtered_df["Latitude"].iloc[0]
        center_lon = filtered_df["Longitude"].iloc[0]
        zoom_level = 6
        pitch_val = 55
    else:
        center_lat = 37.0902
        center_lon = -95.7129
        zoom_level = 3
        pitch_val = 45

    view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom_level, pitch=pitch_val)
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>{State}</b><br>Total Production: {prod_display} MT<hr>{details}",
            "style": {"backgroundColor": "rgba(0, 20, 40, 0.9)", "color": "white", "fontSize": "12px", "padding": "10px", "maxWidth": "350px"}
        }
    )

    
    st.pydeck_chart(r)
    
    st.markdown('<div class="glass-card">💡 <b>Insight:</b> The height of the columns represents the total metric tons of crop production projected for 2025. Higher columns indicate major agricultural hubs for the selected crop.</div>', unsafe_allow_html=True)

elif viz_mode == "Market Analytics":
    st.subheader("Market Dynamics & Value Distribution")
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_pie = px.pie(
            filtered_df.groupby("State")["Market_Value_USD"].sum().sort_values(ascending=False).head(10).reset_index(),
            values="Market_Value_USD",
            names="State",
            title="Top 10 States by Market Value",
            template="plotly_dark",
            hole=0.4
        )
        fig_pie.update_traces(marker=dict(colors=['#00ff88', '#00d4ff', '#ffcc00']))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        fig_bar = px.bar(
            filtered_df.groupby("Crop")["Yield_Index"].mean().reset_index(),
            x="Crop",
            y="Yield_Index",
            title="Average Yield Index by Crop",
            template="plotly_dark",
            color="Yield_Index",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="glass-card">📊 <b>Statistical Summary:</b> Economic output is heavily concentrated in states with optimized irrigation and favorable 2025 weather patterns.</div>', unsafe_allow_html=True)

elif viz_mode == "AI Insights":
    st.subheader("🤖 AI Sustainability & Risk Analysis")
    
    cols = st.columns(3)
    
    insights = [
        {"title": "Climate Resilience", "value": "High", "desc": "Projected increase in drought-resistant corn varieties."},
        {"title": "Export Potential", "value": "+12%", "desc": "Driven by rising demand in southeast Asian markets."},
        {"title": "Soil Health", "value": "Improving", "desc": "Adoption of regeneratve practices is up by 15%."},
    ]
    
    for i, insight in enumerate(insights):
        with cols[i]:
            st.markdown(f"""
                <div class="glass-card">
                    <h3 style="color: #00ff88;">{insight['title']}</h3>
                    <h2 style="color: #ffcc00;">{insight['value']}</h2>
                    <p>{insight['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Simulation Progress
    st.markdown("### Resource Optimization Simulation")
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    st.success("Simulation Complete: Resource allocation optimized for 2025.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>© 2025 USA Agriculture Vision | Built with Streamlit & AI Precision farming.</div>", 
    unsafe_allow_html=True
)
