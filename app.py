import streamlit as st
import pandas as pd
from src.database import get_all_jobs, get_rush_orders, get_overdue_jobs, get_department_summary
from src.analytics import get_kpis
from src.ai_summary import generate_summary

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ops Center · Mifab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F5F5F0;
    color: #1A1A1A;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1400px; }

/* Top bar */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #1A1A1A;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}
.topbar-title {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #1A1A1A;
}
.topbar-sub {
    font-size: 0.78rem;
    color: #666;
    font-weight: 400;
    letter-spacing: 0.04em;
    margin-top: 2px;
}
.topbar-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #888;
}

/* KPI Strip */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: #1A1A1A;
    border: 1px solid #1A1A1A;
    margin-bottom: 2rem;
}
.kpi-cell {
    background: #FAFAF7;
    padding: 1.2rem 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
}
.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #1A1A1A;
    line-height: 1;
}
.kpi-value.alert  { color: #C0392B; }
.kpi-value.warn   { color: #E67E22; }
.kpi-value.ok     { color: #27AE60; }

/* Section headers */
.section-header {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    border-bottom: 1px solid #DDD;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    margin-top: 2rem;
}

/* Status dot */
.dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 6px;
    position: relative;
    top: -1px;
}
.dot-red    { background: #C0392B; }
.dot-amber  { background: #E67E22; }
.dot-green  { background: #27AE60; }
.dot-blue   { background: #2980B9; }
.dot-grey   { background: #BDC3C7; }

/* AI briefing box */
.briefing-box {
    background: #1A1A1A;
    color: #E8E8E0;
    padding: 1.6rem 2rem;
    font-size: 0.92rem;
    line-height: 1.75;
    font-weight: 300;
    border-left: 3px solid #F4A820;
    margin-bottom: 0.5rem;
}
.briefing-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #F4A820;
    margin-bottom: 0.6rem;
}

/* Tables */
.dataframe {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    border: none !important;
}
thead tr th {
    background: #1A1A1A !important;
    color: #F5F5F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 0.8rem !important;
    border: none !important;
}
tbody tr td {
    padding: 0.5rem 0.8rem !important;
    border-color: #EBEBEB !important;
    background: #FAFAF7 !important;
}
tbody tr:hover td { background: #F0F0EA !important; }

/* Generate button */
div.stButton > button {
    background: #1A1A1A;
    color: #F5F5F0;
    border: none;
    border-radius: 0;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.65rem 1.6rem;
    cursor: pointer;
    transition: background 0.15s ease;
}
div.stButton > button:hover {
    background: #333;
    color: #F5F5F0;
    border: none;
}

/* Rush order tag */
.rush-tag {
    display: inline-block;
    background: #C0392B;
    color: white;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 6px;
    margin-left: 6px;
}

/* Divider */
hr { border: none; border-top: 1px solid #DDD; margin: 2rem 0; }

/* Spinner */
.stSpinner > div { border-top-color: #1A1A1A !important; }

</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
df           = get_all_jobs()
rush_orders  = get_rush_orders()
overdue_jobs = get_overdue_jobs()
dept_summary = get_department_summary()
kpis         = get_kpis(df)

from datetime import datetime
today_str = datetime.now().strftime("%A, %d %B %Y  ·  %H:%M")


# ── Top bar ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div>
    <div class="topbar-title">Mifab · Operations Center</div>
    <div class="topbar-sub">Manufacturing & Warehouse Intelligence</div>
  </div>
  <div class="topbar-date">{today_str}</div>
</div>
""", unsafe_allow_html=True)


# ── KPI strip ──────────────────────────────────────────────────────────────────
overdue_class  = "alert" if kpis['overdue'] > 0 else "ok"
rush_class     = "warn"  if kpis['rush'] > 0    else "ok"
complete_class = "ok"    if kpis['completed'] > 0 else "grey"

st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-cell">
    <div class="kpi-label">Total Jobs</div>
    <div class="kpi-value">{kpis['total']}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Completed</div>
    <div class="kpi-value {complete_class}">{kpis['completed']}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Rush Orders</div>
    <div class="kpi-value {rush_class}">{kpis['rush']}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Overdue</div>
    <div class="kpi-value {overdue_class}">{kpis['overdue']}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Avg Build (hrs)</div>
    <div class="kpi-value">{kpis['avg_hours']}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── AI Morning Briefing ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Morning Briefing</div>', unsafe_allow_html=True)

col_btn, col_note = st.columns([1, 5])
with col_btn:
    run_briefing = st.button("Generate Briefing")
with col_note:
    st.markdown(
        "<p style='font-size:0.78rem; color:#999; margin-top:0.6rem;'>"
        "Pulls live job data and generates an ops summary via Claude.</p>",
        unsafe_allow_html=True
    )

if run_briefing:
    with st.spinner("Analysing shop floor data..."):
        summary = generate_summary(kpis, rush_orders, overdue_jobs)
    st.markdown(f"""
    <div class="briefing-box">
      <div class="briefing-label">AI · Ops Summary</div>
      {summary}
    </div>
    """, unsafe_allow_html=True)


# ── Rush Orders + Overdue ──────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

with col_left:
    rush_count = len(rush_orders)
    st.markdown(
        f'<div class="section-header">'
        f'<span class="dot dot-red"></span>Rush Orders'
        f'<span style="float:right;font-family:JetBrains Mono,monospace">{rush_count}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    if rush_count > 0:
        st.dataframe(
            rush_orders[['job_id','customer_name','product','due_date','status']],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.markdown(
            "<p style='font-size:0.82rem;color:#888;padding:0.5rem 0;'>"
            "No rush orders active.</p>",
            unsafe_allow_html=True
        )

with col_right:
    overdue_count = len(overdue_jobs)
    st.markdown(
        f'<div class="section-header">'
        f'<span class="dot dot-amber"></span>Overdue Jobs'
        f'<span style="float:right;font-family:JetBrains Mono,monospace">{overdue_count}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    if overdue_count > 0:
        st.dataframe(
            overdue_jobs[['job_id','customer_name','product','due_date','status']],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.markdown(
            "<p style='font-size:0.82rem;color:#888;padding:0.5rem 0;'>"
            "All jobs on schedule.</p>",
            unsafe_allow_html=True
        )


# ── Department Performance ─────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header">'
    '<span class="dot dot-blue"></span>Department Performance'
    '</div>',
    unsafe_allow_html=True
)
st.dataframe(dept_summary, use_container_width=True, hide_index=True)


# ── Full Job Register ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header">'
    '<span class="dot dot-grey"></span>Full Job Register'
    '</div>',
    unsafe_allow_html=True
)

status_filter = st.selectbox(
    "",
    options=["All", "Complete", "In Progress", "Pending"],
    label_visibility="collapsed"
)

filtered_df = df if status_filter == "All" else df[df['status'] == status_filter]

st.dataframe(
    filtered_df[[
        'job_id','customer_name','product','category',
        'department','due_date','status','rush_order',
        'estimated_build_hours','actual_build_hours'
    ]],
    use_container_width=True,
    hide_index=True,
)

st.markdown(
    f"<p style='font-size:0.7rem;color:#AAA;margin-top:0.5rem;'>"
    f"Showing {len(filtered_df)} of {len(df)} records · "
    f"Source: operations.db · Refreshed {today_str}</p>",
    unsafe_allow_html=True
)