"""
🚦 Indian Roads Accident Analysis Dashboard
Streamlit + Plotly interactive dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from preprocess import load_and_clean, get_summary_stats

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🚦 Indian Roads Accident Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2a2f45);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #e74c3c;
        margin: 4px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #e74c3c; }
    .metric-label { font-size: 0.85rem; color: #8892b0; margin-top: 4px; }
    .section-header {
        font-size: 1.2rem; font-weight: 600;
        color: #cdd6f4; margin: 16px 0 8px 0;
        border-bottom: 2px solid #e74c3c;
        padding-bottom: 4px;
    }
    [data-testid="stSidebar"] { background-color: #161b2e; }
    .stSelectbox > div > div { background-color: #1e2130; }
</style>
""", unsafe_allow_html=True)

# ─── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    return load_and_clean(os.path.join(base, "indian_roads_dataset.xlsx"))

df = load_data()

# ─── Color palettes ──────────────────────────────────────────────────────────
SEVERITY_COLORS = {"minor": "#27ae60", "major": "#f39c12", "fatal": "#e74c3c"}
CAUSE_COLORS    = px.colors.qualitative.Bold
PLOTLY_TEMPLATE = "plotly_dark"

# ─── Sidebar filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    states = ["All"] + sorted(df['state'].cat.categories.tolist())
    sel_state = st.selectbox("📍 State", states)

    if sel_state != "All":
        cities = ["All"] + sorted(df[df['state'] == sel_state]['city'].cat.categories.tolist())
    else:
        cities = ["All"] + sorted(df['city'].cat.categories.tolist())
    sel_city = st.selectbox("🏙️ City", cities)

    sel_severity = st.multiselect(
        "⚠️ Severity",
        options=["minor", "major", "fatal"],
        default=["minor", "major", "fatal"]
    )

    sel_road = st.multiselect(
        "🛣️ Road Type",
        options=df['road_type'].cat.categories.tolist(),
        default=df['road_type'].cat.categories.tolist()
    )

    sel_weather = st.multiselect(
        "🌤️ Weather",
        options=df['weather'].cat.categories.tolist(),
        default=df['weather'].cat.categories.tolist()
    )

    year_min, year_max = int(df['year'].min()), int(df['year'].max())
    sel_years = st.slider("📅 Year Range", year_min, year_max, (year_min, year_max))

    st.markdown("---")
    st.markdown("**🇮🇳 Indian Roads**\nAccident Analysis Dashboard")

# ─── Apply filters ────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_state != "All":
    filtered = filtered[filtered['state'] == sel_state]
if sel_city != "All":
    filtered = filtered[filtered['city'] == sel_city]
if sel_severity:
    filtered = filtered[filtered['accident_severity'].isin(sel_severity)]
if sel_road:
    filtered = filtered[filtered['road_type'].isin(sel_road)]
if sel_weather:
    filtered = filtered[filtered['weather'].isin(sel_weather)]
filtered = filtered[(filtered['year'] >= sel_years[0]) & (filtered['year'] <= sel_years[1])]

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🚦 Indian Roads Accident Analysis")
st.markdown(f"**{len(filtered):,}** records selected · Data: 2023–2024")
st.markdown("---")

# ─── KPI cards ───────────────────────────────────────────────────────────────
stats = get_summary_stats(filtered)

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "🚗", f"{stats['total_accidents']:,}", "Total Accidents"),
    (c2, "💀", f"{stats['total_casualties']:,}", "Total Casualties"),
    (c3, "🚙", f"{stats['total_vehicles']:,}", "Vehicles Involved"),
    (c4, "🔴", f"{stats['fatal_pct']}%", "Fatal Accidents"),
    (c5, "⚡", f"{stats['avg_risk']}", "Avg Risk Score"),
    (c6, "🕐", f"{stats['peak_hour_pct']}%", "During Peak Hours"),
]
for col, icon, val, label in kpis:
    col.markdown(f"""
    <div class="metric-card">
      <div style="font-size:1.5rem">{icon}</div>
      <div class="metric-value">{val}</div>
      <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ─── Row 1: Severity + Cause ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">⚠️ Accidents by Severity</div>', unsafe_allow_html=True)
    sev_df = filtered['accident_severity'].value_counts().reset_index()
    sev_df.columns = ['Severity', 'Count']
    fig = px.pie(sev_df, names='Severity', values='Count',
                 color='Severity', color_discrete_map=SEVERITY_COLORS,
                 hole=0.45, template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(margin=dict(t=10, b=10), height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">🎯 Accidents by Cause</div>', unsafe_allow_html=True)
    cause_df = filtered['cause'].value_counts().reset_index()
    cause_df.columns = ['Cause', 'Count']
    fig = px.bar(cause_df, x='Count', y='Cause', orientation='h',
                 color='Cause', color_discrete_sequence=CAUSE_COLORS,
                 template=PLOTLY_TEMPLATE)
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10), height=300,
                      yaxis_title="", xaxis_title="Number of Accidents")
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 2: Time trends ──────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">📅 Monthly Accident Trend</div>', unsafe_allow_html=True)
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly = (filtered.groupby(['month_name','accident_severity'])
               .size().reset_index(name='Count'))
    monthly['month_name'] = pd.Categorical(monthly['month_name'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('month_name')
    fig = px.line(monthly, x='month_name', y='Count',
                  color='accident_severity', color_discrete_map=SEVERITY_COLORS,
                  markers=True, template=PLOTLY_TEMPLATE)
    fig.update_layout(margin=dict(t=10, b=10), height=300,
                      xaxis_title="", yaxis_title="Accidents", legend_title="Severity")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">🕐 Accidents by Hour of Day</div>', unsafe_allow_html=True)
    hourly = filtered.groupby('hour').size().reset_index(name='Count')
    fig = px.bar(hourly, x='hour', y='Count',
                 color='Count', color_continuous_scale='Reds',
                 template=PLOTLY_TEMPLATE)
    fig.update_layout(margin=dict(t=10, b=10), height=300,
                      xaxis_title="Hour (0–23)", yaxis_title="Accidents",
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 3: State heatmap + Weather ──────────────────────────────────────────
col5, col6 = st.columns([3, 2])

with col5:
    st.markdown('<div class="section-header">🗺️ State-wise Accident Heatmap</div>', unsafe_allow_html=True)
    state_sev = (filtered.groupby(['state','accident_severity'])
                 .size().unstack(fill_value=0).reset_index())
    state_sev['Total'] = state_sev[['minor','major','fatal']].sum(axis=1)
    state_sev = state_sev.sort_values('Total', ascending=False)

    fig = go.Figure()
    for sev, color in SEVERITY_COLORS.items():
        if sev in state_sev.columns:
            fig.add_trace(go.Bar(
                name=sev.capitalize(), x=state_sev['state'],
                y=state_sev[sev], marker_color=color
            ))
    fig.update_layout(barmode='stack', template=PLOTLY_TEMPLATE,
                      margin=dict(t=10, b=10), height=320,
                      xaxis_title="", yaxis_title="Accidents", legend_title="Severity")
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">🌤️ Weather Impact on Severity</div>', unsafe_allow_html=True)
    wdf = (filtered.groupby(['weather','accident_severity'])
           .size().reset_index(name='Count'))
    fig = px.bar(wdf, x='weather', y='Count', color='accident_severity',
                 barmode='group', color_discrete_map=SEVERITY_COLORS,
                 template=PLOTLY_TEMPLATE)
    fig.update_layout(margin=dict(t=10, b=10), height=320,
                      xaxis_title="", yaxis_title="Accidents", legend_title="Severity")
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 4: Road type + Risk distribution ────────────────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.markdown('<div class="section-header">🛣️ Road Type vs Casualties</div>', unsafe_allow_html=True)
    rt = filtered.groupby('road_type').agg(
        Accidents=('accident_id','count'),
        Casualties=('casualties','sum'),
        AvgRisk=('risk_score','mean')
    ).reset_index()
    fig = px.scatter(rt, x='Accidents', y='Casualties',
                     size='AvgRisk', color='road_type',
                     text='road_type',
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     template=PLOTLY_TEMPLATE, size_max=50)
    fig.update_traces(textposition='top center')
    fig.update_layout(margin=dict(t=10, b=10), height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col8:
    st.markdown('<div class="section-header">📊 Risk Score Distribution</div>', unsafe_allow_html=True)
    fig = px.histogram(filtered, x='risk_score', color='accident_severity',
                       nbins=30, barmode='overlay',
                       color_discrete_map=SEVERITY_COLORS,
                       template=PLOTLY_TEMPLATE, opacity=0.75)
    fig.update_layout(margin=dict(t=10, b=10), height=300,
                      xaxis_title="Risk Score", yaxis_title="Count",
                      legend_title="Severity")
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 5: Day of week + Festival ──────────────────────────────────────────
col9, col10 = st.columns(2)

with col9:
    st.markdown('<div class="section-header">📆 Day-of-Week Pattern</div>', unsafe_allow_html=True)
    dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = filtered['day_of_week'].value_counts().reindex(dow_order).reset_index()
    dow.columns = ['Day', 'Count']
    colors = ['#e74c3c' if d in ['Saturday','Sunday'] else '#4a9eff' for d in dow['Day']]
    fig = px.bar(dow, x='Day', y='Count', template=PLOTLY_TEMPLATE,
                 color_discrete_sequence=['#4a9eff'])
    fig.update_traces(marker_color=colors)
    fig.update_layout(margin=dict(t=10, b=10), height=280, xaxis_title="", yaxis_title="Accidents")
    st.plotly_chart(fig, use_container_width=True)

with col10:
    st.markdown('<div class="section-header">🎉 Festival vs Non-Festival Accidents</div>', unsafe_allow_html=True)
    fest = (filtered.groupby('festival').agg(
        Accidents=('accident_id','count'),
        AvgCasualties=('casualties','mean'),
        AvgRisk=('risk_score','mean')
    ).reset_index().sort_values('Accidents', ascending=False))
    fig = px.bar(fest, x='festival', y='Accidents',
                 color='AvgRisk', color_continuous_scale='RdYlGn_r',
                 template=PLOTLY_TEMPLATE, text='Accidents')
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(margin=dict(t=10, b=30), height=280,
                      xaxis_title="", yaxis_title="Accidents",
                      coloraxis_colorbar_title="Avg Risk")
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 6: Map ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ Geographic Accident Map</div>', unsafe_allow_html=True)
map_sample = filtered.sample(min(3000, len(filtered)), random_state=42)
fig_map = px.scatter_mapbox(
    map_sample,
    lat='latitude', lon='longitude',
    color='accident_severity',
    color_discrete_map=SEVERITY_COLORS,
    size='risk_score',
    hover_data=['city','state','cause','casualties'],
    zoom=4.5, center={"lat": 20.5, "lon": 78.9},
    mapbox_style='carto-darkmatter',
    template=PLOTLY_TEMPLATE,
    opacity=0.7,
    height=480,
)
fig_map.update_layout(margin=dict(t=10, b=10), legend_title="Severity")
st.plotly_chart(fig_map, use_container_width=True)

# ─── Data table ──────────────────────────────────────────────────────────────
with st.expander("📋 View Cleaned Data Table"):
    display_cols = ['accident_id','city','state','date','road_type','weather',
                    'cause','accident_severity','casualties','vehicles_involved',
                    'risk_score','risk_category','time_of_day','festival']
    st.dataframe(
        filtered[display_cols].sort_values('date', ascending=False).head(500),
        use_container_width=True,
        height=350
    )

    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Cleaned Data (CSV)",
        data=csv,
        file_name="indian_roads_cleaned.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown(
    "<center style='color:#8892b0;font-size:0.8rem'>🚦 Indian Roads Accident Dashboard · "
    "Built with Streamlit & Plotly · Data: 20,000 Accident Records</center>",
    unsafe_allow_html=True
)
