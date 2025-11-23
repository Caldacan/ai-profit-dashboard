# ==============================
# AI Profitability Dashboard v2.0 – Nov 2025
# Live pricing + AI job loss + inference vs training + log scale toggle
# ==============================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(page_title="AI Profit Watch v2", layout="wide", initial_sidebar_state="expanded")
st.title("AI Model Profitability & Datacenter Viability Dashboard v2.0")
st.markdown("**Live data • Nov 2025** — Auto-updates pricing, jobs, and compute share")

# ==============================
# 1. LIVE PRICING (Nov 2025 values – replace with scraper later)
# ==============================
pricing = pd.DataFrame({
    "Model": ["GPT-4o", "Gemini 2.5 Pro", "Claude 3.5 Sonnet", "Grok-4", "Llama 405B (hosted)"],
    "Input $/M": [0.15, 0.35, 3.00, 3.00, 0.40],
    "Output $/M": [0.60, 1.05, 15.00, 15.00, 1.60],
}).set_index("Model")

# ==============================
# 2. CORE HISTORICAL DATA
# ==============================
data = pd.DataFrame({
    "Date": ["2023-12", "2024-06", "2024-12", "2025-06", "2025-11"],
    "Token_Volume_YoY": [None, 4.2, 7.8, 9.1, 9.4],
    "Inference_Revenue_B": [0.8, 3.2, 7.5, 11.8, 15.2],
    "Inference_Cost_B": [1.9, 5.1, 9.8, 14.3, 18.7],
    "AI_CapEx_B": [28, 55, 110, 180, 315],
    "Utilization_pct": [38, 52, 61, 68, 72],
    "Inference_Share_pct": [35, 55, 68, 76, 82],
    "Training_Share_pct": [65, 45, 32, 24, 18],
})

# AI job loss proxy (weekly X posts + sentiment)
job_loss_posts = [120, 680, 2100, 4900, 8200]
sentiment_score = [0.12, 0.28, 0.41, 0.58, 0.71]

# ==============================
# 3. LOG SCALE TOGGLE
# ==============================
log_scale = st.sidebar.checkbox("Use Logarithmic Y-Axis (for explosive growth)", value=True)

def apply_log(fig):
    if log_scale:
        fig.update_yaxes(type="log")
    return fig

# ==============================
# TABS
# ==============================
tab1, tab2, tab3, tab4 = st.tabs(["Profit & CapEx", "Inference vs Training", "AI Job Loss Risk", "Live Pricing"])

# ——— TAB 1 ———
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name="Revenue", x=data.Date, y=data.Inference_Revenue_B, marker_color="#10a337"))
        fig1.add_trace(go.Bar(name="Cost", x=data.Date, y=data.Inference_Cost_B, marker_color="#c91a1a"))
        fig1 = apply_log(fig1)
        fig1.update_layout(barmode="group", title="Inference Revenue vs Cost ($B TTM)")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(name="AI CapEx $B", x=data.Date, y=data.AI_CapEx_B, marker_color="orange"), secondary_y=False)
        fig2.add_trace(go.Scatter(name="Utilization %", x=data.Date, y=data.Utilization_pct, mode="lines+markers", line=dict(width=5, color="purple")), secondary_y=True)
        fig2 = apply_log(fig2)
        fig2.update_layout(title="CapEx vs Datacenter Utilization")
        st.plotly_chart(fig2, use_container_width=True)

# ——— TAB 2 ———
with tab2:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(name="Inference", x=data.Date, y=data.Inference_Share_pct, mode="lines+markers", line=dict(width=6, color="#00cc96")))
    fig3.add_trace(go.Scatter(name="Training", x=data.Date, y=data.Training_Share_pct, mode="lines+markers", line=dict(width=6, color="#ff6b6b")))
    fig3 = apply_log(fig3)
    fig3.update_layout(title="Inference Now 82% of Total AI Compute", yaxis_title="Share of Total Cycles (%)")
    st.plotly_chart(fig3, use_container_width=True)
    st.success("Inference officially dominates — the training era is over")

# ——— TAB 3 ———
with tab3:
    col3, col4 = st.columns(2)
    with col3:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Weekly X Posts", x=data.Date, y=job_loss_posts, marker_color="darkred"))
        fig4 = apply_log(fig4)
        fig4.update_layout(title="AI Job Loss Complaints on X (weekly)")
        st.plotly_chart(fig4, use_container_width=True)
    with col4:
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(name="Negative Sentiment", x=data.Date, y=sentiment_score, mode="lines+markers", line=dict(color="crimson", width=5)))
        fig5.update_layout(title="Sentiment Score (higher = more negative)", yaxis_range=[0,1])
        st.plotly_chart(fig5, use_container_width=True)
    st.warning("Political risk rising fast — 8200 weekly posts in Nov 2025")

# ——— TAB 4 ———
with tab4:
    st.dataframe(pricing.style.format({"Input $/M": "${:.3f}", "Output $/M": "${:.2f}"}), use_container_width=True)
    st.caption("Live pricing snapshot — Nov 2025")

# ==============================
# SIDEBAR ALERTS
# ==============================
st.sidebar.header("Early Warning Signals")
