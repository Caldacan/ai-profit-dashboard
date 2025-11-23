# ==============================
# AI Profitability & Datacenter Viability Dashboard
# Run with: streamlit run ai_dashboard.py
# ==============================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Inference Profit Watch", layout="wide")
st.title("AI Model Profitability & Datacenter Viability Dashboard")
st.markdown("**Nov 2025 snapshot** – Updated quarterly from earnings & API pricing")

# ==============================
# 1. DATA (update these rows every quarter)
# ==============================

data = pd.DataFrame({
    "Date": [
        "2023-12", "2024-06", "2024-12", "2025-06", "2025-11"
    ],
    # Token volume growth YoY (Azure OpenAI = proxy for market)
    "Token_Volume_YoY": [None, 4.2, 7.8, 9.1, 9.4],
    
    # Inference revenue (OpenAI + Anthropic + xAI + Google est.)
    "Inference_Revenue_B": [0.8, 3.2, 7.5, 11.8, 15.2],
    
    # Total inference compute cost (training + inference spend)
    "Inference_Cost_B": [1.9, 5.1, 9.8, 14.3, 18.7],
    
    # Hyperscaler AI capex (MSFT + GOOG + AMZN + META)
    "AI_CapEx_B": [28, 55, 110, 180, 315],
    
    # Datacenter utilization (industry avg, Bain/IDC)
    "Utilization_pct": [38, 52, 61, 68, 72],
    
    # Avg inference cost per million tokens (blended flagship)
    "Cost_per_M_Tokens": [1.80, 0.62, 0.19, 0.09, 0.07],
    
    # Avg revenue per million tokens (blended)
    "Revenue_per_M_Tokens": [2.10, 1.10, 0.65, 0.48, 0.41]
})

# Individual model pricing (Nov 2025)
pricing = pd.DataFrame({
    "Model": ["GPT-4o", "Gemini 2.5 Pro", "Claude 3.5 Sonnet", "Grok-4", "Llama 405B (hosted)"],
    "Input $/M": [0.15, 0.35, 3.00, 3.00, 0.40],
    "Output $/M": [0.60, 1.05, 15.00, 15.00, 1.60],
    "Total $/M (avg query)": [0.36, 0.63, 7.50, 7.50, 0.88]
}).set_index("Model")

# ==============================
# 2. DASHBOARD LAYOUT
# ==============================

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Inference Profit Gap (Revenue – Cost)")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="Revenue", x=data.Date, y=data.Inference_Revenue_B, marker_color="#10a337"))
    fig1.add_trace(go.Bar(name="Cost",   x=data.Date, y=data.Inference_Cost_B,   marker_color="#c91a1a"))
    fig1.update_layout(barmode="group", title="OpenAI + Anthropic + xAI + Google inference P&L ($B TTM)")
    st.plotly_chart(fig1, use_container_width=True)

    st.metric(
        label="Inference Profit Gap (Nov 2025)",
        value=f"${data.Inference_Revenue_B.iloc[-1] - data.Inference_Cost_B.iloc[-1]:.1f}B",
        delta=f"{((data.Inference_Revenue_B.iloc[-1]/data.Inference_Cost_B.iloc[-1])-1)*100:.0f}% margin"
    )

with col2:
    st.subheader("2. Datacenter Utilization vs. CapEx Explosion")
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(name="AI CapEx $B", x=data.Date, y=data.AI_CapEx_B, marker_color="orange"), secondary_y=False)
    fig2.add_trace(go.Scatter(name="Utilization %", x=data.Date, y=data.Utilization_pct, mode="lines+markers", line=dict(width=5, color="purple")), secondary_y=True)
    fig2.update_yaxes(title_text="CapEx ($B)", secondary_y=False)
    fig2.update_yaxes(title_text="Utilization (%)", secondary_y=True, range=[0,100])
    fig2.update_layout(title="Hyperscaler AI CapEx vs. Datacenter Utilization")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Token Volume Growth (YoY) – The Demand Engine")
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=data.Date, y=data.Token_Volume_YoY, mode="lines+markers", line=dict(width=6, color="#00cc96")))
fig3.update_layout(title="Azure OpenAI Token Volume Growth (YoY multiple)", yaxis_title="x times prior year")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Price Deflation Race – Revenue vs Cost per Million Tokens")
fig4 = make_subplots(specs=[[{"secondary_y": True}]])
fig4.add_trace(go.Scatter(name="Revenue/M tokens", x=data.Date, y=data.Revenue_per_M_Tokens, mode="lines+markers", line=dict(color="green")), secondary_y=False)
fig4.add_trace(go.Scatter(name="Cost/M tokens",    x=data.Date, y=data.Cost_per_M_Tokens,    mode="lines+markers", line=dict(color="red")), secondary_y=True)
fig4.update_yaxes(title_text="Revenue per M tokens ($)", secondary_y=False)
fig4.update_yaxes(title_text="Cost per M tokens ($)", secondary_y=True)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Current API Pricing Comparison (Nov 2025)")
st.dataframe(pricing.style.format({"Input $/M": "${:.2f}", "Output $/M": "${:.2f}", "Total $/M (avg query)": "${:.2f}"}))

# ==============================
# 6. WARNING SYSTEM
# ==============================

st.subheader("Early-Warning Signals")
col_a, col_b, col_c = st.columns(3)

with col_a:
    if data.Utilization_pct.iloc[-1] < 65:
        st.error(f"Utilization {data.Utilization_pct.iloc[-1]}% → Dark GPU risk")
    else:
        st.success(f"Utilization {data.Utilization_pct.iloc[-1]}% → Healthy")

with col_b:
    margin = data.Inference_Revenue_B.iloc[-1] / data.Inference_Cost_B.iloc[-1]
    if margin < 1.0:
        st.error(f"Inference margin {margin:.1f}x → Still burning cash")
    elif margin < 1.3:
        st.warning(f"Inference margin {margin:.1f}x → Breakeven near")
    else:
        st.success(f"Inference margin {margin:.1f}x → Profitable")

with col_c:
    if data.Token_Volume_YoY.iloc[-1] < 5:
        st.error("Token growth slowing → Demand cliff")
    else:
        st.success(f"Token growth {data.Token_Volume_YoY.iloc[-1]:.1f}x → Still exploding")

st.caption("Data sources: MSFT/Google earnings, OpenAI leaks, Epoch AI, Bain, Sacra, company API pages – Nov 2025")
