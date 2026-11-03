"""
Bank Marketing Campaign — EDA Dashboard
Pink / magenta / plum theme matching the project design.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Theme tokens (from design mockup)
# ---------------------------------------------------------------------------
PINK = "#EC4899"
PINK_SOFT = "#F9A8D4"
PINK_LIGHT = "#FCE7F3"
PINK_DEEP = "#DB2777"
PLUM = "#4A1942"
PLUM_SOFT = "#6B3A5E"
BG = "#FFF1F5"
WHITE = "#FFFFFF"
TEXT = "#3B0A2A"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="Segoe UI, sans-serif", size=13),
    margin=dict(l=40, r=20, t=50, b=40),
    colorway=[PINK, PINK_SOFT, PLUM, "#F472B6", "#9D174D", "#BE185D"],
)


@st.cache_data
def load_data():
    path = Path("data") / "bank.csv"
    df = pd.read_csv(path)
    # Treat literal "unknown" as incomplete for cleaning view (kept as category in analysis)
    return df


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .stApp {{
            background: linear-gradient(180deg, {BG} 0%, #FFE4F0 55%, #FFD6E8 100%);
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PLUM} 0%, #3A1235 100%) !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: #FFE4F0 !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiSelect label,
        section[data-testid="stSidebar"] .stSlider label {{
            color: #FBCFE8 !important;
            font-weight: 600;
        }}

        div[data-baseweb="select"] > div {{
            background-color: {PLUM_SOFT} !important;
            border-radius: 12px !important;
            border: 1px solid #EC489955 !important;
        }}

        .hero-title {{
            font-size: 1.85rem;
            font-weight: 800;
            color: {PLUM};
            margin-bottom: 0.15rem;
            line-height: 1.25;
        }}
        .hero-sub {{
            color: {PLUM_SOFT};
            font-size: 0.98rem;
            margin-bottom: 0.6rem;
        }}
        .pill {{
            display: inline-block;
            background: linear-gradient(90deg, {PINK}, {PINK_DEEP});
            color: white !important;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            box-shadow: 0 6px 16px rgba(236, 72, 153, 0.35);
        }}

        .kpi-card {{
            background: {WHITE};
            border-radius: 22px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 10px 28px rgba(74, 25, 66, 0.08);
            border: 1px solid #FBCFE8;
            text-align: center;
            height: 100%;
        }}
        .kpi-icon {{
            width: 42px; height: 42px;
            border-radius: 14px;
            display: inline-flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, {PINK_SOFT}, {PINK});
            color: white; font-size: 1.2rem; margin-bottom: 0.4rem;
        }}
        .kpi-value {{
            font-size: 1.75rem; font-weight: 800; color: {PLUM}; margin: 0;
        }}
        .kpi-label {{
            font-size: 0.85rem; color: {PLUM_SOFT}; font-weight: 600; margin: 0;
        }}

        .panel {{
            background: {WHITE};
            border-radius: 22px;
            padding: 1rem 1.1rem 0.6rem 1.1rem;
            box-shadow: 0 10px 28px rgba(74, 25, 66, 0.08);
            border: 1px solid #FBCFE8;
            margin-bottom: 1rem;
        }}
        .panel-title {{
            font-weight: 800; color: {PLUM}; font-size: 1.05rem; margin: 0 0 0.4rem 0;
        }}

        .insight-box {{
            background: {WHITE};
            border-radius: 22px;
            padding: 1.2rem 1.3rem;
            box-shadow: 0 10px 28px rgba(74, 25, 66, 0.08);
            border: 1px solid #FBCFE8;
        }}
        .insight-box h3 {{
            color: {PLUM}; margin-top: 0; font-weight: 800;
        }}
        .insight-box li {{
            color: {PLUM_SOFT}; margin-bottom: 0.45rem; font-weight: 500;
        }}

        .side-brand {{
            text-align: center; padding: 0.5rem 0 1rem 0;
        }}
        .side-brand h2 {{
            color: #FFF !important; font-size: 1.15rem; font-weight: 800; margin: 0.4rem 0 0 0;
        }}
        .side-card {{
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(249,168,212,0.35);
            border-radius: 16px;
            padding: 0.85rem;
            margin-top: 1rem;
            font-size: 0.85rem;
        }}

        /* Hide default Streamlit chrome noise */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(icon: str, value: str, label: str) -> str:
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <p class="kpi-value">{value}</p>
        <p class="kpi-label">{label}</p>
    </div>
    """


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown(
        """
        <div class="side-brand">
            <div style="font-size:2.2rem;">🏦</div>
            <h2>Bank Marketing EDA</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Customer Analysis", "Campaign Insights", "Subscription Analysis", "About"],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")

    jobs = sorted(df["job"].unique().tolist())
    selected_jobs = st.sidebar.multiselect("Job", jobs, default=jobs)

    marital_opts = sorted(df["marital"].unique().tolist())
    selected_marital = st.sidebar.multiselect("Marital status", marital_opts, default=marital_opts)

    edu_opts = sorted(df["education"].unique().tolist())
    selected_edu = st.sidebar.multiselect("Education", edu_opts, default=edu_opts)

    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

    months = [
        "jan", "feb", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "oct", "nov", "dec",
    ]
    present_months = [m for m in months if m in set(df["month"])]
    selected_months = st.sidebar.multiselect("Contact month", present_months, default=present_months)

    deposit_filter = st.sidebar.selectbox("Subscription (deposit)", ["All", "yes", "no"])

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
        <div class="side-card">
            <strong>Project</strong><br/>
            Exploring customer patterns in bank marketing campaigns.
        </div>
        """,
        unsafe_allow_html=True,
    )
    return filtered, page


def subscription_donut(df: pd.DataFrame):
    counts = df["deposit"].value_counts().rename(index={"yes": "Subscribed", "no": "Not Subscribed"})
    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts.index,
                values=counts.values,
                hole=0.62,
                marker=dict(colors=[PINK, PINK_SOFT]),
                textinfo="percent",
                textfont=dict(size=14, color=PLUM),
            )
        ]
    )
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, height=320, title="Subscription Rate")
    return fig


def age_hist(df: pd.DataFrame):
    fig = px.histogram(
        df,
        x="age",
        nbins=25,
        color_discrete_sequence=[PINK],
        title="Age Distribution",
    )
    fig.update_traces(marker_line_color=WHITE, marker_line_width=0.5)
    fig.update_layout(**PLOTLY_LAYOUT, height=320, bargap=0.05)
    fig.update_xaxes(title="Age", gridcolor="#FBCFE8")
    fig.update_yaxes(title="Count", gridcolor="#FBCFE8")
    return fig


def job_outcome(df: pd.DataFrame):
    ct = (
        df.groupby(["job", "deposit"])
        .size()
        .reset_index(name="count")
        .replace({"deposit": {"yes": "Subscribed", "no": "Not Subscribed"}})
    )
    fig = px.bar(
        ct,
        x="job",
        y="count",
        color="deposit",
        barmode="group",
        color_discrete_map={"Subscribed": PINK, "Not Subscribed": PINK_SOFT},
        title="Campaign Outcome by Job",
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=320, xaxis_tickangle=-35)
    fig.update_xaxes(title="Job", gridcolor="#FBCFE8")
    fig.update_yaxes(title="Customers", gridcolor="#FBCFE8")
    return fig


def contact_donut(df: pd.DataFrame):
    counts = df["contact"].value_counts()
    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts.index.str.title(),
                values=counts.values,
                hole=0.58,
                marker=dict(colors=[PINK, PINK_SOFT, PLUM_SOFT]),
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=320, title="Contact Type Analysis")
    return fig


def balance_by_deposit(df: pd.DataFrame):
    plot_df = df.copy()
    plot_df["deposit_label"] = plot_df["deposit"].map({"yes": "Subscribed", "no": "Not Subscribed"})
    fig = px.box(
        plot_df,
        x="deposit_label",
        y="balance",
        color="deposit_label",
        color_discrete_map={"Subscribed": PINK, "Not Subscribed": PINK_SOFT},
        title="Account Balance by Subscription",
        points=False,
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=360, showlegend=False)
    fig.update_yaxes(title="Balance", gridcolor="#FBCFE8")
    fig.update_xaxes(title="")
    return fig


def duration_scatter(df: pd.DataFrame):
    sample = df.sample(min(2500, len(df)), random_state=42) if len(df) else df
    sample = sample.copy()
    sample["deposit_label"] = sample["deposit"].map({"yes": "Subscribed", "no": "Not Subscribed"})
    fig = px.scatter(
        sample,
        x="duration",
        y="balance",
        color="deposit_label",
        color_discrete_map={"Subscribed": PINK, "Not Subscribed": PLUM_SOFT},
        opacity=0.55,
        title="Call Duration vs Balance",
        hover_data=["age", "job"],
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=360)
    fig.update_xaxes(title="Duration (seconds)", gridcolor="#FBCFE8")
    fig.update_yaxes(title="Balance", gridcolor="#FBCFE8")
    return fig


def month_sub_rate(df: pd.DataFrame):
    order = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    tmp = (
        df.groupby("month")["deposit"]
        .apply(lambda s: (s == "yes").mean() * 100)
        .reindex([m for m in order if m in df["month"].unique()])
        .reset_index(name="rate")
    )
    fig = px.bar(
        tmp,
        x="month",
        y="rate",
        color="rate",
        color_continuous_scale=["#FCE7F3", PINK, PLUM],
        title="Subscription Rate by Month (%)",
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=360, coloraxis_showscale=False)
    fig.update_xaxes(title="Month")
    fig.update_yaxes(title="Subscription rate (%)", gridcolor="#FBCFE8")
    return fig


def corr_heatmap(df: pd.DataFrame):
    nums = df.select_dtypes(include=np.number)
    corr = nums.corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale=["#FCE7F3", PINK_SOFT, PINK, PLUM],
        title="Numeric Feature Correlation",
        aspect="auto",
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=420)
    return fig


def education_compare(df: pd.DataFrame):
    rate = (
        df.groupby("education")["deposit"]
        .apply(lambda s: (s == "yes").mean() * 100)
        .reset_index(name="rate")
        .sort_values("rate", ascending=False)
    )
    fig = px.bar(
        rate,
        x="education",
        y="rate",
        color="rate",
        color_continuous_scale=["#FCE7F3", PINK],
        title="Subscription Rate by Education (%)",
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=360, coloraxis_showscale=False)
    fig.update_yaxes(title="Rate (%)", gridcolor="#FBCFE8")
    fig.update_xaxes(title="Education")
    return fig


def render_overview(df: pd.DataFrame, full_n: int):
    n = len(df)
    sub_rate = (df["deposit"] == "yes").mean() * 100 if n else 0
    no_rate = 100 - sub_rate
    features = df.shape[1] - 1

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("👥", f"{n:,}", "Total Customers"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("📢", f"{sub_rate:.1f}%", "Subscribed"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("📉", f"{no_rate:.1f}%", "Did Not Subscribe"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("⭐", f"{features}", "Features"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="panel"><p class="panel-title">Subscription Rate</p></div>', unsafe_allow_html=True)
        st.plotly_chart(subscription_donut(df), use_container_width=True)
    with g2:
        st.markdown('<div class="panel"><p class="panel-title">Age Distribution</p></div>', unsafe_allow_html=True)
        st.plotly_chart(age_hist(df), use_container_width=True)
    with g3:
        st.markdown('<div class="panel"><p class="panel-title">Campaign Outcome by Job</p></div>', unsafe_allow_html=True)
        st.plotly_chart(job_outcome(df), use_container_width=True)

    b1, b2 = st.columns([1.2, 1])
    with b1:
        st.markdown(
            f"""
            <div class="insight-box">
                <h3>💡 Key Insights</h3>
                <ul>
                    <li>Filtered view shows <b>{sub_rate:.1f}%</b> subscription rate
                        (full data: {full_n:,} rows).</li>
                    <li>Young and middle-aged customers are the largest contacted group.</li>
                    <li>Job type and contact channel clearly shift subscription odds.</li>
                    <li>Longer call duration strongly tracks with a “yes” outcome.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown('<div class="panel"><p class="panel-title">Contact Type Analysis</p></div>', unsafe_allow_html=True)
        st.plotly_chart(contact_donut(df), use_container_width=True)


def render_customer(df: pd.DataFrame):
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(age_hist(df), use_container_width=True)
        st.plotly_chart(education_compare(df), use_container_width=True)
    with c2:
        st.plotly_chart(balance_by_deposit(df), use_container_width=True)
        marital = (
            df.groupby("marital")["deposit"]
            .apply(lambda s: (s == "yes").mean() * 100)
            .reset_index(name="rate")
        )
        fig = px.bar(
            marital,
            x="marital",
            y="rate",
            color_discrete_sequence=[PINK],
            title="Subscription Rate by Marital Status (%)",
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=360)
        fig.update_yaxes(gridcolor="#FBCFE8")
        st.plotly_chart(fig, use_container_width=True)


def render_campaign(df: pd.DataFrame):
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(month_sub_rate(df), use_container_width=True)
        st.plotly_chart(contact_donut(df), use_container_width=True)
    with c2:
        st.plotly_chart(duration_scatter(df), use_container_width=True)
        camp = df.copy()
        camp["campaign_bin"] = pd.cut(
            camp["campaign"],
            bins=[0, 1, 2, 3, 5, 10, 100],
            labels=["1", "2", "3", "4-5", "6-10", "11+"],
        )
        rate = (
            camp.groupby("campaign_bin", observed=True)["deposit"]
            .apply(lambda s: (s == "yes").mean() * 100)
            .reset_index(name="rate")
        )
        fig = px.line(
            rate,
            x="campaign_bin",
            y="rate",
            markers=True,
            title="Subscription Rate vs Number of Contacts",
            color_discrete_sequence=[PINK_DEEP],
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=360)
        fig.update_yaxes(title="Rate (%)", gridcolor="#FBCFE8")
        fig.update_xaxes(title="Campaign contacts")
        st.plotly_chart(fig, use_container_width=True)


def render_subscription(df: pd.DataFrame):
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(subscription_donut(df), use_container_width=True)
        st.plotly_chart(job_outcome(df), use_container_width=True)
    with c2:
        st.plotly_chart(corr_heatmap(df), use_container_width=True)
        housing = (
            df.groupby("housing")["deposit"]
            .apply(lambda s: (s == "yes").mean() * 100)
            .reset_index(name="rate")
        )
        fig = px.bar(
            housing,
            x="housing",
            y="rate",
            color="housing",
            color_discrete_sequence=[PINK, PINK_SOFT],
            title="Subscription Rate by Housing Loan (%)",
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def render_about():
    st.markdown(
        f"""
        <div class="insight-box">
            <h3>About this project</h3>
            <p style="color:{PLUM_SOFT};">
                This dashboard explores the Bank Marketing Campaign dataset to understand
                which customer and campaign factors link to term-deposit subscriptions.
            </p>
            <ul>
                <li><b>Source:</b> UCI / Kaggle Bank Marketing data</li>
                <li><b>Rows × columns:</b> 11,162 × 17</li>
                <li><b>Target:</b> deposit (yes / no)</li>
                <li><b>Stack:</b> Python, Pandas, Plotly, Streamlit</li>
            </ul>
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
    filtered, page = apply_filters(df)

    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
            <div>
                <div class="hero-title">Bank Marketing Campaign — Exploratory Data Analysis (EDA) Dashboard</div>
                <div class="hero-sub">Understand which customers subscribe to a term deposit after a marketing call.</div>
            </div>
            <div class="pill">Dataset: {len(df):,} Records • {df.shape[1]} Features</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Showing **{len(filtered):,}** rows after filters.")

    if page == "Overview":
        render_overview(filtered, len(df))
    elif page == "Customer Analysis":
        render_customer(filtered)
    elif page == "Campaign Insights":
        render_campaign(filtered)
    elif page == "Subscription Analysis":
        render_subscription(filtered)
    else:
        render_about()

    st.markdown("---")
    show_raw = st.checkbox("Show raw data")
    if show_raw:
        st.dataframe(filtered, use_container_width=True)

    st.markdown(
        f"""
        <div class="insight-box" style="margin-top:1rem;">
            <h3>📌 Findings</h3>
            <ul>
                <li><b>Duration matters:</b> longer calls strongly align with subscriptions.</li>
                <li><b>Housing loan = lower yes rate:</b> customers without a housing loan subscribe more often.</li>
                <li><b>Prior success helps:</b> previous campaign success (poutcome) lifts conversion.</li>
            </ul>
            <p style="color:{PINK_DEEP}; font-weight:700;">
                Suggestion: prioritise cellular outreach to customers with no housing loan,
                and invest call time in high-intent conversations rather than more contacts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
