# app.py
"""
EcoStream-Agent: Autonomous Multi-Agent AI for Methane Mitigation & Prescriptive Maintenance
-----------------------------------------------------------------------------------------
The production-ready Streamlit dashboard fully integrated with the LangGraph Backend.
"""

from __future__ import annotations
import math
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st

# استيراد محرك الوكلاء والإعدادات المركزية من مشروعك
from config import Config
from agents.graph import app_graph

# ---------------------------------------------------------------------------
# 1. إعدادات الصفحة الأساسية (Streamlit configuration)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoStream-Agent 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. الهوية البصرية والثيم المظلم للمؤسسات (Custom Corporate CSS)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top left, #0f2027 0%, #14323b 35%, #0b1f24 100%);
            color: #e6edf3;
        }
        .hero {
            background: linear-gradient(135deg, rgba(13,110,253,0.25), rgba(25,135,84,0.18));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 22px 28px;
            margin-bottom: 8px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.45);
        }
        .hero h1 { margin: 0 0 4px 0; font-size: 2.4rem; letter-spacing: -0.5px; }
        .hero p { margin: 0; color: #9fb4c2; font-size: 1.05rem; }
        .pill {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 5px 12px; border-radius: 999px; font-weight: 600;
            font-size: 0.82rem; letter-spacing: 0.3px;
            border: 1px solid rgba(46,204,113,0.45); background: rgba(46,204,113,0.12); color: #2ecc71;
        }
        .pill .dot {
            width: 8px; height: 8px; border-radius: 50%; background: #2ecc71;
            box-shadow: 0 0 8px #2ecc71; animation: blink 1.6s infinite;
        }
        @keyframes blink { 50% { opacity: 0.35; } }
        .agent-card {
            background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px; padding: 16px 18px; height: 100%; backdrop-filter: blur(4px);
        }
        .card-accent { height: 3px; border-radius: 3px; margin-bottom: 12px; }
        .kpi {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px; padding: 12px 14px; margin: 6px 0;
        }
        .kpi .label { font-size: 0.75rem; color: #8aa0ae; text-transform: uppercase; letter-spacing: 0.6px; }
        .kpi .value { font-size: 1.45rem; font-weight: 700; margin-top: 2px; }
        .sev-low { color: #2ecc71; }
        .sev-med { color: #f1c40f; }
        .sev-high { color: #ff4d4f; }
        .scada-log {
            font-family: 'JetBrains Mono','Consolas',monospace; font-size: 0.8rem; background: #060f13;
            border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px 12px;
            color: #7ee787; white-space: pre-wrap; max-height: 180px; overflow-y: auto;
        }
        .section-h { font-size: 1.15rem; font-weight: 700; margin: 18px 0 8px 0; color: #e6edf3; }
        [data-testid="stMetric"] { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 10px 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 3. دالات الرسوم البيانية التخطيطية (UI Visualization Helpers)
# ---------------------------------------------------------------------------
def build_pressure_timeline(pressure_psi: float, leak_rate: float, n_points: int = 60) -> pd.DataFrame:
    drop_factor = leak_rate / 100.0
    t = np.arange(n_points)
    decay = pressure_psi * (1 - 0.18 * drop_factor * (t / n_points))
    noise = np.random.normal(0, max(2.0, pressure_psi * 0.004), n_points)
    return pd.DataFrame({"Time (s)": t, "Pipeline Pressure (PSI)": np.clip(decay + noise, 0, None)})

def build_leak_timeline(leak_rate: float, n_points: int = 60) -> pd.DataFrame:
    t = np.arange(n_points)
    wave = leak_rate * (0.85 + 0.15 * np.sin(t / 5.0))
    noise = np.random.normal(0, max(0.4, leak_rate * 0.03), n_points)
    return pd.DataFrame({"Time (s)": t, "CH₄ Leak Rate (kg/hr)": np.clip(wave + noise, 0, None)})

# ---------------------------------------------------------------------------
# 4. الهيدر وشريط الحالة
# ---------------------------------------------------------------------------
st.markdown('<div class="hero"><h1>🚀 EcoStream-Agent</h1><p>Autonomous Multi-Agent System for Methane Leak Mitigation &amp; Automated Dispatch</p></div>', unsafe_allow_html=True)
st.markdown('<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px;"><span class="pill"><span class="dot"></span> System Status: ACTIVE</span><span class="pill"><span class="dot"></span> All Agents: ONLINE</span><span class="pill"><span class="dot"></span> Edge-to-Cloud Link: SECURED</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 5. لوحة التحكم الجانبية (Sidebar Controllers & Session State)
# ---------------------------------------------------------------------------
if "leak_rate_slider" not in st.session_state:
    st.session_state.leak_rate_slider = 12.0
if "pressure_slider" not in st.session_state:
    st.session_state.pressure_slider = 650.0

with st.sidebar:
    st.markdown("### 🎛️ Simulation Controls")
    st.caption("Adjust real-time operating conditions to drive the agents.")

    leak_rate = st.slider("🟡 Methane Leak Rate (kg/hr)", 0.0, 100.0, key="leak_rate_slider")
    pressure = st.slider("🔵 Pipeline Pressure (PSI)", 300.0, 1000.0, key="pressure_slider")

    st.markdown("---")
    st.markdown("#### 📷 Upload Thermal / Optical Image")
    uploaded = st.file_uploader("Upload Thermal/Optical Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    image_bytes = uploaded.read() if uploaded else None

    st.markdown("---")
    if st.button("🔴 Simulate Critical Leak Event", use_container_width=True, type="primary"):
        st.session_state.leak_rate_slider = 78.0
        st.session_state.pressure_slider = 880.0
        st.rerun()

    if st.button("↩️ Reset to Baseline", use_container_width=True):
        st.session_state.leak_rate_slider = 12.0
        st.session_state.pressure_slider = 650.0
        st.rerun()

# ---------------------------------------------------------------------------
# 6. تشغيل محرك الوكلاء الخلفي الحقيقي (LangGraph Execution)
# ---------------------------------------------------------------------------
with st.spinner("🧠 Orchestrating Agents Communication Flow via LangGraph..."):
    # تمرير الحالات الحية للمؤشرات إلى الـ Graph الخاص بك
    final_state = app_graph.invoke({
        "leak_rate": leak_rate,
        "pressure": pressure,
        "image_bytes": image_bytes,
        "logs": []
    })

risk = final_state.get("esg_risk_level", "Low")
accent_color = {"Low": "#2ecc71", "Medium": "#f1c40f", "High": "#ff4d4f"}[risk]
risk_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[risk]
risk_class = {"Low": "sev-low", "Medium": "sev-med", "High": "sev-high"}[risk]

# ---------------------------------------------------------------------------
# 7. عرض البيانات بعد معالجة الوكلاء لها (Agent Row Visualization)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-h">🤖 Multi-Agent Orchestration Dashboard</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3, gap="medium")

# ── الوكيل الأول: وكيل الرصد والاستشعار (Monitor Agent)
with col1:
    st.markdown('<div class="agent-card"><div class="card-accent" style="background:#3b82f6;"></div><h3 style="margin:0 0 2px 0;">👁️ Agent 1 — Multimodal Monitor</h3><span style="color:#8aa0ae;font-size:0.8rem;">Detection &amp; Sensing Layer</span></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**📊 Pipeline Pressure Telemetry**")
        st.line_chart(build_pressure_timeline(pressure, leak_rate), x="Time (s)", y="Pipeline Pressure (PSI)", use_container_width=True)

        st.markdown("**🌫️ Methane Concentration (CH₄)**")
        st.line_chart(build_leak_timeline(leak_rate), x="Time (s)", y="CH₄ Leak Rate (kg/hr)", use_container_width=True)

        # عرض المخرجات الحقيقية القادمة من عقدة المراقبة (Monitor Node)
        st.markdown(f"""
            <div class="kpi">
              <div class="label">Visual Inspection Summary</div>
              <div class="value" style="font-size:0.95rem; font-weight:normal; color:#9fb4c2;">{final_state['visual_analysis_summary']}</div>
            </div>
            <div class="kpi">
              <div class="label">Sensor Telemetry Status</div>
              <div class="value {'sev-high' if final_state['anomaly_detected'] else 'sev-low'}">{final_state['telemetry_status']}</div>
            </div>
        """, unsafe_allow_html=True)

        # توليد مصفوفة الخريطة الحرارية المحسنة فائق السرعة عبر NumPy (Vectorized)
        st.markdown("**CNG Thermal Gradient Plume**")
        y_grid, x_grid = np.ogrid[:60, :120]
        dist = np.hypot(x_grid - 80, y_grid - 30)
        v_gradient = np.maximum(0.0, 1.0 - dist / 50.0) * (leak_rate / 100.0)
        heat_map = np.zeros((60, 120, 3), dtype=int)
        heat_map[..., 0] = np.clip(255 * np.minimum(1, v_gradient * 2), 0, 255)
        heat_map[..., 1] = np.clip(255 * v_gradient, 0, 255)
        heat_map[..., 2] = np.clip(80 * v_gradient, 0, 255)
        st.image(heat_map, use_container_width=True, clamp=True)

# ── الوكيل الثاني: وكيل تقييم المخاطر والاستدامة (Risk & ESG Agent)
with col2:
    st.markdown('<div class="agent-card"><div class="card-accent" style="background:#a855f7;"></div><h3 style="margin:0 0 2px 0;">🧮 Agent 2 — Risk &amp; ESG Assessment</h3><span style="color:#8aa0ae;font-size:0.8rem;">Financial &amp; Environmental Impact</span></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**🔬 Carbon Tax Penalty Formula**")
        st.latex(r"\text{CO}_2\text{e} = \dot{m}_{\text{CH}_4} \times \text{GWP}_{\text{CH}_4}")
        st.caption(f"with GWP_CH₄ = {Config.METHANE_GWP}  •  Carbon tax = ${Config.CARBON_TAX_PER_TONNE_CO2E:.0f}/t")

        # عرض الأرقام الحقيقية المحسوبة في الـ Backend
        st.markdown(f"""
            <div class="kpi"><div class="label">Estimated Gas Lost Cost</div><div class="value">${final_state['gas_lost_cost_hourly']:.2f} <span style="font-size:0.8rem;color:#8aa0ae;">/hr</span></div></div>
            <div class="kpi"><div class="label">Carbon Emissions Penalty</div><div class="value">${final_state['carbon_penalty_hourly']:.2f} <span style="font-size:0.8rem;color:#8aa0ae;">/hr</span></div></div>
            <div class="kpi"><div class="label">CO₂-equivalent Rate</div><div class="value">{final_state['co2_equivalent_rate']:.1f} <span style="font-size:0.8rem;color:#8aa0ae;">kg CO₂e/hr</span></div></div>
            <div class="kpi"><div class="label">ESG Risk Level</div><div class="value {risk_class}">{risk_emoji} {risk}</div></div>
        """, unsafe_allow_html=True)

# ── الوكيل الثالث: وكيل التنفيذ والتحكم (Action & Orchestration Agent)
with col3:
    st.markdown(f'<div class="agent-card"><div class="card-accent" style="background:{accent_color};"></div><h3 style="margin:0 0 2px 0;">⚡ Agent 3 — Action &amp; Orchestration</h3><span style="color:#8aa0ae;font-size:0.8rem;">Prescriptive Response &amp; Dispatch</span></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**🛠️ Autonomous SCADA Action Gateway**")
        st.markdown(f'<div class="scada-log">{final_state["scada_log"]}</div>', unsafe_allow_html=True)

        st.markdown("**🔍 CMMS Inventory Database Lookup**")
        if final_state["inventory_available"]:
            st.success("✅ Part Found: Replacement Valve Kit is active and pre-staged by CMMS Agent.", icon="📦")
        else:
            st.info("CMMS query idle — no pipeline components required.", icon="📦")

        st.markdown("**📧 Automated Telemetry Field Dispatch**")
        if leak_rate >= 5.0:
            st.success(f"📨 Work order dispatched via API: **{Config.TECH_NAME}** (ETA: {Config.TECH_CONTACT.split(' ')[0]} - ~11 min).", icon="🚐")
        else:
            st.info("No dispatch execution required for baseline operations.", icon="🚐")

# ---------------------------------------------------------------------------
# 8. قسم الدليل التشغيلي المولد بالـ AI والسجلات (AI Runbook Generator & Logs)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-h">📄 Automated AI Dispatch Report Generator</div>', unsafe_allow_html=True)
with st.expander("🤖 View Generative AI Technical Repair Runbook", expanded=(risk == "High")):
    left, right = st.columns([3, 1])
    with left:
        st.markdown("Runbook dynamically generated from live Gemini models using context parameters:")
        st.code(final_state["generated_runbook"], language="text")
    with right:
        st.markdown("#### 📋 Shared Execution Logs")
        # طباعة سجل حركة البيانات المشتركة بين عقد الـ LangGraph
        log_text = "\n".join(final_state.get("logs", []))
        st.markdown(f'<div class="scada-log" style="height:160px; color:#a855f7;">{log_text}</div>', unsafe_allow_html=True)
        
        st.download_button(
            "⬇️ Download Runbook (.txt)",
            data=final_state["generated_runbook"],
            file_name=f"EcoStream_Runbook_V102_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.markdown("---")
st.caption("EcoStream-Agent • Advanced Enterprise Multi-Agent AI Architecture • Built for Next-Gen ESG Compliance.")