"""
Bank Marketing Campaign — EDA Dashboard
Green theme (same layout, green palette).
"""

from pathlib import Path
import base64

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Green palette (same roles as before)
PINK = "#2E7D32"       # primary green
PINK_HOT = "#43A047"
PINK_MID = "#66BB6A"
PINK_SOFT = "#A5D6A7"
PINK_PALE = "#E8F5E9"
PINK_BG = "#F1F8F4"
PLUM = "#0D3B2E"        # deep forest (sidebar / headings)
PLUM_DEEP = "#06281F"
TEXT = "#0D3B2E"
MUTED = "#5A7A68"
WHITE = "#FFFFFF"

PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="Poppins, sans-serif", size=11),
    margin=dict(l=28, r=12, t=10, b=28),
)


@st.cache_data
def load_data():
    return pd.read_csv(Path("data") / "bank.csv")


def svg_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def inject_css():
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif !important; }}

.stApp {{
  background: {PINK_BG} !important;
}}
.stApp::before {{
  content: "";
  position: fixed; right: 0; bottom: 0; width: 42vw; height: 34vh;
  background: radial-gradient(ellipse at bottom right, #A5D6A7 0%, #81C78488 35%, transparent 70%);
  pointer-events: none; z-index: 0;
}}
.block-container {{
  padding-top: 1.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 1200px;
  position: relative; z-index: 1;
}}

/* ===== SIDEBAR (vivid green / forest) ===== */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
  background: transparent !important;
}}
section[data-testid="stSidebar"] {{
  min-width: 280px !important;
  background:
    radial-gradient(ellipse 140% 60% at 50% 115%, #66BB6A 0%, #43A047 22%, #2E7D32AA 42%, transparent 62%),
    radial-gradient(ellipse 90% 45% at -10% -5%, #A5D6A7 0%, transparent 50%),
    linear-gradient(170deg, #1B5E40 0%, #145239 28%, #0D3B2E 65%, #06281F 100%) !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
  background: transparent !important;
  padding: 1.2rem 1rem 1.75rem 1rem;
}}
section[data-testid="stSidebar"] * {{ color: #E8F5E9 !important; }}
section[data-testid="stSidebar"] hr {{
  border: none !important;
  height: 2px !important;
  background: linear-gradient(90deg, transparent, #81C784, #43A047, #81C784, transparent) !important;
  margin: 1rem 0 !important;
  opacity: 0.85;
}}

/* Nav radio = mockup menu */
section[data-testid="stSidebar"] div[role="radiogroup"] {{ gap: 0.5rem; }}
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
  background: rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
  padding: 0.82rem 1.05rem !important;
  margin: 0 !important;
  border: 1px solid rgba(129,199,132,0.28) !important;
  backdrop-filter: blur(6px);
  transition: 0.2s ease;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
  background: rgba(67,160,71,0.40) !important;
  border-color: rgba(165,214,167,0.7) !important;
  box-shadow: 0 6px 18px rgba(46,125,50,0.35);
  transform: translateX(4px);
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
  background: linear-gradient(100deg, #81C784 0%, #43A047 40%, #2E7D32 100%) !important;
  border-color: rgba(255,255,255,0.35) !important;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.2) inset,
              0 12px 32px rgba(46,125,50,0.65),
              0 0 36px rgba(67,160,71,0.45);
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {{
  color: #fff !important;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label span {{
  font-weight: 700 !important; font-size: 0.96rem !important;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] p {{
  font-size: 0.96rem !important; font-weight: 700 !important; letter-spacing: 0.01em;
  color: #F1F8F4 !important;
}}

section[data-testid="stSidebar"] .stExpander {{
  background: linear-gradient(145deg, rgba(67,160,71,0.32), rgba(255,255,255,0.10));
  border-radius: 16px;
  border: 1px solid rgba(129,199,132,0.5) !important;
  box-shadow: 0 8px 22px rgba(0,0,0,0.2), inset 0 0 28px rgba(67,160,71,0.12);
}}
section[data-testid="stSidebar"] label {{ font-weight: 600 !important; color: #C8E6C9 !important; }}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
  background: rgba(255,255,255,0.16) !important;
  border-radius: 12px !important;
  border-color: rgba(129,199,132,0.55) !important;
}}

.brand {{
  display: flex; align-items: center; gap: 0.8rem;
  padding: 0.4rem 0.35rem 1.35rem 0.35rem;
}}
.brand-icon {{
  width: 54px; height: 54px; border-radius: 18px;
  background: linear-gradient(145deg, #C8E6C9, #66BB6A 40%, #2E7D32);
  display: grid; place-items: center; font-size: 1.5rem;
  box-shadow: 0 0 0 4px rgba(129,199,132,0.35),
              0 12px 28px rgba(46,125,50,0.65),
              0 0 40px rgba(67,160,71,0.55);
}}
.brand h1 {{
  margin: 0; color: #fff !important; font-size: 1.12rem; font-weight: 800; line-height: 1.25;
  text-shadow: 0 2px 16px rgba(67,160,71,0.55);
}}

.project-card {{
  margin-top: 1.6rem;
  background: linear-gradient(155deg, rgba(67,160,71,0.45) 0%, rgba(46,125,50,0.22) 45%, rgba(255,255,255,0.10) 100%);
  border: 1px solid rgba(165,214,167,0.55);
  border-radius: 18px;
  padding: 1.05rem 1.1rem;
  font-size: 0.82rem; line-height: 1.5;
  box-shadow: 0 12px 28px rgba(0,0,0,0.25),
              inset 0 1px 0 rgba(255,255,255,0.22),
              0 0 24px rgba(67,160,71,0.2);
}}
.project-card .pt {{ color: #fff !important; font-weight: 800; font-size: 0.95rem; margin-bottom: 0.4rem; }}
.project-card .heart {{
  color: #A5D6A7 !important; margin-top: 0.55rem; font-size: 1.15rem;
  text-shadow: 0 0 16px rgba(129,199,132,1);
}}

/* ===== MAIN ===== */
.hero {{
  display: flex; justify-content: space-between; align-items: flex-start;
  gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;
}}
.hero h1 {{
  margin: 0; font-size: 1.85rem; font-weight: 800; color: {PLUM}; line-height: 1.15;
}}
.hero p {{
  margin: 0.2rem 0 0 0; color: {MUTED}; font-size: 0.95rem; font-weight: 500;
}}
.badge {{
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: {WHITE}; color: {PLUM};
  border: 1px solid #A5D6A7; border-radius: 999px;
  padding: 0.45rem 0.95rem; font-size: 0.78rem; font-weight: 600;
  box-shadow: 0 6px 16px rgba(45,27,51,0.06);
}}

.kpi {{
  background: {WHITE}; border-radius: 18px;
  border: 1px solid #A5D6A7;
  box-shadow: 0 10px 26px rgba(13,59,46,0.06);
  padding: 0.95rem 1rem; display: flex; align-items: center; gap: 0.85rem;
  min-height: 88px;
}}
.kpi .ic {{
  width: 46px; height: 46px; min-width: 46px; border-radius: 14px;
  display: grid; place-items: center; font-size: 1.2rem; color: #fff;
  background: linear-gradient(145deg, #81C784, #2E7D32);
  box-shadow: 0 8px 16px rgba(46,125,50,0.28);
}}
.kpi .ic.gold {{
  background: linear-gradient(145deg, #FFE082, #FFB300);
  box-shadow: 0 8px 16px rgba(255,179,0,0.28);
}}
.kpi .v {{ margin: 0; font-size: 1.45rem; font-weight: 800; color: {PLUM}; line-height: 1.1; }}
.kpi .l {{ margin: 0.12rem 0 0 0; font-size: 0.76rem; color: {MUTED}; font-weight: 500; }}

.card {{
  background: {WHITE}; border-radius: 20px;
  border: 1px solid #A5D6A7;
  box-shadow: 0 10px 26px rgba(13,59,46,0.06);
  padding: 0.85rem 0.95rem 0.4rem 0.95rem;
  height: 100%;
}}
.card h3 {{
  margin: 0 0 0.15rem 0; font-size: 0.95rem; font-weight: 700; color: {PLUM};
}}

.insights {{
  background: {WHITE}; border-radius: 20px;
  border: 1px solid #A5D6A7;
  box-shadow: 0 10px 26px rgba(13,59,46,0.06);
  padding: 1.1rem 1.15rem; height: 100%;
}}
.insights h3 {{
  margin: 0 0 0.85rem 0; font-size: 1rem; font-weight: 700; color: {PLUM};
}}
.ins-row {{
  display: flex; gap: 0.65rem; align-items: flex-start; margin-bottom: 0.75rem;
}}
.ins-ic {{
  width: 26px; height: 26px; min-width: 26px; border-radius: 50%;
  background: linear-gradient(145deg, #81C784, #2E7D32);
  color: #fff; font-size: 0.72rem; display: grid; place-items: center;
}}
.ins-txt {{ color: {MUTED}; font-size: 0.86rem; font-weight: 500; line-height: 1.4; }}

.decor {{
  position: fixed; right: 18px; bottom: 8px; width: 200px; opacity: 0.88;
  pointer-events: none; z-index: 0; filter: none;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
div[data-testid="stToolbar"] {{ display: none; }}
</style>
        """,
        unsafe_allow_html=True,
    )


def kpi(icon, value, label, gold=False):
    cls = "ic gold" if gold else "ic"
    return f"""
    <div class="kpi">
      <div class="{cls}">{icon}</div>
      <div><p class="v">{value}</p><p class="l">{label}</p></div>
    </div>"""


def fig_donut_sub(df):
    yes = int((df["deposit"] == "yes").sum())
    no = int((df["deposit"] == "no").sum())
    fig = go.Figure(go.Pie(
        labels=["Yes", "No"], values=[yes, no], hole=0.66, sort=False,
        marker=dict(colors=[PINK, PINK_SOFT], line=dict(color=WHITE, width=4)),
        textinfo="percent", textposition="outside",
        textfont=dict(size=12, color=TEXT, family="Poppins"),
    ))
    fig.update_layout(**PLOTLY, height=265, showlegend=True,
                      legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center",
                                  font=dict(size=11)))
    return fig


def fig_age(df):
    fig = px.histogram(df, x="age", nbins=22, color_discrete_sequence=[PINK_MID])
    fig.update_traces(marker_line_color=WHITE, marker_line_width=1)
    fig.update_layout(**PLOTLY, height=265, bargap=0.1, showlegend=False)
    fig.update_xaxes(title="Age", gridcolor="#A5D6A7", showgrid=True, zeroline=False)
    fig.update_yaxes(title="Count", gridcolor="#A5D6A7", showgrid=True, zeroline=False)
    return fig


def fig_job(df):
    # Match mockup jobs subset order if present
    preferred = ["admin.", "blue-collar", "entrepreneur", "services",
                 "student", "technician", "unemployed", "management",
                 "retired", "self-employed", "housemaid", "unknown"]
    ct = (
        df.groupby(["job", "deposit"]).size().reset_index(name="count")
        .replace({"deposit": {"yes": "Subscribed", "no": "Not Subscribed"}})
    )
    present = [j for j in preferred if j in set(ct["job"])]
    ct["job"] = pd.Categorical(ct["job"], categories=present, ordered=True)
    ct = ct.sort_values("job")
    fig = px.bar(
        ct, x="job", y="count", color="deposit", barmode="group",
        color_discrete_map={"Subscribed": PINK, "Not Subscribed": PINK_SOFT},
    )
    fig.update_layout(**PLOTLY, height=265, showlegend=True,
                      legend=dict(orientation="h", y=-0.42, title=None, font=dict(size=10)),
                      xaxis_tickangle=-25)
    fig.update_xaxes(title="", gridcolor="#A5D6A7")
    fig.update_yaxes(title="", gridcolor="#A5D6A7")
    return fig


def fig_contact(df):
    counts = df["contact"].value_counts()
    # Order: cellular, telephone, unknown like mockup legend feel
    order = [c for c in ["cellular", "telephone", "unknown"] if c in counts.index]
    order += [c for c in counts.index if c not in order]
    vals = [counts[c] for c in order]
    labels = [c.title() for c in order]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.64, sort=False,
        marker=dict(colors=[PINK, PINK_SOFT, "#80CBC4"][: len(order)],
                    line=dict(color=WHITE, width=4)),
        textinfo="none",
    ))
    fig.update_layout(**PLOTLY, height=265, showlegend=True,
                      legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center",
                                  font=dict(size=11)))
    return fig


def fig_balance(df):
    d = df.copy()
    d["label"] = d["deposit"].map({"yes": "Subscribed", "no": "Not Subscribed"})
    fig = px.box(d, x="label", y="balance", color="label",
                 color_discrete_map={"Subscribed": PINK, "Not Subscribed": PINK_SOFT}, points=False)
    fig.update_layout(**PLOTLY, height=320, showlegend=False)
    fig.update_xaxes(title=""); fig.update_yaxes(title="Balance", gridcolor="#A5D6A7")
    return fig


def fig_scatter(df):
    s = df.sample(min(2500, len(df)), random_state=42).copy() if len(df) else df.copy()
    s["label"] = s["deposit"].map({"yes": "Subscribed", "no": "Not Subscribed"})
    fig = px.scatter(s, x="duration", y="balance", color="label",
                     color_discrete_map={"Subscribed": PINK, "Not Subscribed": "#1B5E20"},
                     opacity=0.55, hover_data=["age", "job"])
    fig.update_layout(**PLOTLY, height=320)
    fig.update_xaxes(title="Duration (seconds)", gridcolor="#A5D6A7")
    fig.update_yaxes(title="Balance", gridcolor="#A5D6A7")
    return fig


def fig_month(df):
    order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    tmp = (df.groupby("month")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
           .reindex([m for m in order if m in df["month"].unique()]).reset_index(name="rate"))
    fig = px.bar(tmp, x="month", y="rate", color="rate",
                 color_continuous_scale=[PINK_PALE, PINK, PLUM])
    fig.update_layout(**PLOTLY, height=320, coloraxis_showscale=False)
    fig.update_yaxes(title="Rate (%)", gridcolor="#A5D6A7")
    return fig


def fig_corr(df):
    corr = df.select_dtypes(include=np.number).corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=".2f",
                    color_continuous_scale=[PINK_PALE, PINK_SOFT, PINK, PLUM], aspect="auto")
    fig.update_layout(**PLOTLY, height=380)
    return fig


def fig_edu(df):
    rate = (df.groupby("education")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
            .reset_index(name="rate").sort_values("rate", ascending=False))
    fig = px.bar(rate, x="education", y="rate", color="rate",
                 color_continuous_scale=[PINK_PALE, PINK])
    fig.update_layout(**PLOTLY, height=320, coloraxis_showscale=False)
    fig.update_yaxes(title="Rate (%)", gridcolor="#A5D6A7")
    return fig


def sidebar(df):
    st.sidebar.markdown(
        """
        <div class="brand">
          <div class="brand-icon">🏦</div>
          <h1>Bank Marketing<br/>EDA</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "nav",
        ["Overview", "Customer Analysis", "Campaign Insights", "Subscription Analysis", "About"],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Overview": "🏠  Overview",
            "Customer Analysis": "👤  Customer Analysis",
            "Campaign Insights": "📢  Campaign Insights",
            "Subscription Analysis": "📈  Subscription Analysis",
            "About": "ℹ️  About",
        }[x],
    )

    with st.sidebar.expander("Filters", expanded=False):
        jobs = sorted(df["job"].unique().tolist())
        selected_jobs = st.multiselect("Job", jobs, default=jobs)
        marital_opts = sorted(df["marital"].unique().tolist())
        selected_marital = st.multiselect("Marital status", marital_opts, default=marital_opts)
        edu_opts = sorted(df["education"].unique().tolist())
        selected_edu = st.multiselect("Education", edu_opts, default=edu_opts)
        age_min, age_max = int(df["age"].min()), int(df["age"].max())
        age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))
        months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        present = [m for m in months if m in set(df["month"])]
        selected_months = st.multiselect("Contact month", present, default=present)
        deposit_filter = st.selectbox("Subscription", ["All", "yes", "no"])

    filtered = df[
        df["job"].isin(selected_jobs)
        & df["marital"].isin(selected_marital)
        & df["education"].isin(selected_edu)
        & df["age"].between(age_range[0], age_range[1])
        & df["month"].isin(selected_months)
    ].copy()
    if deposit_filter != "All":
        filtered = filtered[filtered["deposit"] == deposit_filter]

    st.sidebar.markdown(
        """
        <div class="project-card">
          <div class="pt">✨ Project</div>
          Exploring customer patterns in bank marketing campaigns.
          <div class="heart">♡</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return filtered, page


def overview(df, full_n):
    n = len(df)
    sub = (df["deposit"] == "yes").mean() * 100 if n else 0
    nos = 100 - sub
    feats = df.shape[1] - 1

    st.markdown(
        f"""
        <div class="hero">
          <div>
            <h1>Bank Marketing Campaign</h1>
            <p>Exploratory Data Analysis (EDA) Dashboard</p>
          </div>
          <div class="badge">🗄️ Dataset: {full_n:,} Records • {df.shape[1]} Features</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    a.markdown(kpi("👥", f"{n:,}", "Total Customers"), unsafe_allow_html=True)
    b.markdown(kpi("📢", f"{sub:.1f}%", "Subscribed"), unsafe_allow_html=True)
    c.markdown(kpi("📈", f"{nos:.1f}%", "Did Not Subscribe"), unsafe_allow_html=True)
    d.markdown(kpi("⭐", f"{feats}", "Features", gold=True), unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="card"><h3>Subscription Rate</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_donut_sub(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="card"><h3>Age Distribution</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_age(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g3:
        st.markdown('<div class="card"><h3>Campaign Outcome by Job</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_job(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown(
            f"""
            <div class="insights">
              <h3>💡 Key Insights</h3>
              <div class="ins-row"><div class="ins-ic">✓</div>
                <div class="ins-txt"><b>{sub:.1f}%</b> of customers subscribed to a term deposit.</div></div>
              <div class="ins-row"><div class="ins-ic">✓</div>
                <div class="ins-txt">Young and middle-aged customers show higher interest.</div></div>
              <div class="ins-row"><div class="ins-ic">✓</div>
                <div class="ins-txt">Blue-collar and technician workers had strong response rates.</div></div>
              <div class="ins-row"><div class="ins-ic">✓</div>
                <div class="ins-txt">Campaign success is influenced by job type, age, and contact type.</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="card"><h3>Contact Type Analysis</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_contact(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Decorative bank (mockup bottom-right)
    bank = Path("assets") / "bank.svg"
    if bank.exists():
        b64 = svg_b64(bank)
        st.markdown(
            f'<img class="decor" src="data:image/svg+xml;base64,{b64}" alt="bank"/>',
            unsafe_allow_html=True,
        )


def page_customer(df):
    st.markdown('<div class="hero"><div><h1>Customer Analysis</h1><p>Who was contacted?</p></div></div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>Age Distribution</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_age(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="card"><h3>Subscription by Education</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_edu(df), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown('<div class="card"><h3>Balance by Subscription</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_balance(df), use_container_width=True, config={"displayModeBar": False})
        marital = (df.groupby("marital")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
                   .reset_index(name="rate"))
        fig = px.bar(marital, x="marital", y="rate", color_discrete_sequence=[PINK])
        fig.update_layout(**PLOTLY, height=320)
        fig.update_yaxes(title="Rate (%)", gridcolor="#A5D6A7")
        st.markdown('<div class="card"><h3>Subscription by Marital Status</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def page_campaign(df):
    st.markdown('<div class="hero"><div><h1>Campaign Insights</h1><p>How the campaign performed</p></div></div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>Subscription Rate by Month</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_month(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="card"><h3>Contact Type Analysis</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_contact(df), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown('<div class="card"><h3>Duration vs Balance</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_scatter(df), use_container_width=True, config={"displayModeBar": False})
        camp = df.copy()
        camp["bin"] = pd.cut(camp["campaign"], bins=[0,1,2,3,5,10,100],
                             labels=["1","2","3","4-5","6-10","11+"])
        rate = (camp.groupby("bin", observed=True)["deposit"]
                .apply(lambda s: (s == "yes").mean() * 100).reset_index(name="rate"))
        fig = px.line(rate, x="bin", y="rate", markers=True, color_discrete_sequence=[PINK])
        fig.update_layout(**PLOTLY, height=320)
        fig.update_yaxes(title="Rate (%)", gridcolor="#A5D6A7")
        st.markdown('<div class="card"><h3>Subscription vs Number of Contacts</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def page_subscription(df):
    st.markdown('<div class="hero"><div><h1>Subscription Analysis</h1><p>What drives a yes?</p></div></div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>Subscription Rate</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_donut_sub(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="card"><h3>Campaign Outcome by Job</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_job(df), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown('<div class="card"><h3>Numeric Correlation</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_corr(df), use_container_width=True, config={"displayModeBar": False})
        housing = (df.groupby("housing")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
                   .reset_index(name="rate"))
        fig = px.bar(housing, x="housing", y="rate", color="housing",
                     color_discrete_sequence=[PINK, PINK_SOFT])
        fig.update_layout(**PLOTLY, height=280, showlegend=False)
        st.markdown('<div class="card"><h3>Subscription by Housing Loan</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def page_about():
    st.markdown(
        f"""
        <div class="insights">
          <h3>About this project</h3>
          <div class="ins-row"><div class="ins-ic">1</div>
            <div class="ins-txt"><b>Source:</b> UCI / Kaggle Bank Marketing data</div></div>
          <div class="ins-row"><div class="ins-ic">2</div>
            <div class="ins-txt"><b>Size:</b> 11,162 rows × 17 columns</div></div>
          <div class="ins-row"><div class="ins-ic">3</div>
            <div class="ins-txt"><b>Target:</b> deposit (yes / no)</div></div>
          <div class="ins-row"><div class="ins-ic">4</div>
            <div class="ins-txt"><b>Stack:</b> Python · Pandas · Plotly · Streamlit</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Bank Marketing EDA Dashboard",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    df = load_data()
    filtered, page = sidebar(df)

    if page == "Overview":
        overview(filtered, len(df))
    elif page == "Customer Analysis":
        page_customer(filtered)
    elif page == "Campaign Insights":
        page_campaign(filtered)
    elif page == "Subscription Analysis":
        page_subscription(filtered)
    else:
        page_about()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    show_raw = st.checkbox("Show raw data")
    if show_raw:
        st.dataframe(filtered, use_container_width=True)

    st.markdown(
        f"""
        <div class="insights" style="margin-top:0.8rem;">
          <h3>📌 Findings</h3>
          <div class="ins-row"><div class="ins-ic">1</div>
            <div class="ins-txt"><b>Duration matters</b> — longer calls strongly align with subscriptions.</div></div>
          <div class="ins-row"><div class="ins-ic">2</div>
            <div class="ins-txt"><b>No housing loan</b> — higher subscription rate than customers with one.</div></div>
          <div class="ins-row"><div class="ins-ic">3</div>
            <div class="ins-txt"><b>Prior success helps</b> — previous campaign success lifts conversion.</div></div>
          <p style="color:{PINK};font-weight:700;margin:0.5rem 0 0 0;font-size:0.88rem;">
            Suggestion: prioritise cellular outreach to customers with no housing loan,
            and invest in call quality over more contacts.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
