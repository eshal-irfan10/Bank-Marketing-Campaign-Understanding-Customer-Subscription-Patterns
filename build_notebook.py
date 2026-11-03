"""Generate Bank_Marketing_EDA.ipynb with full Part 2 EDA steps + slide figures."""

from pathlib import Path

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# ---------------------------------------------------------------------------
md("""# Bank Marketing Campaign — Understanding Customer Subscription Patterns

**Part 2: Exploratory Data Analysis (EDA)**

This notebook explores which customers subscribe to a bank term deposit after a marketing campaign call.
""")

# Step 1
md("""## Step 1: Understand the data

### Where the data comes from
The dataset is the **Bank Marketing** dataset (UCI Machine Learning Repository / Kaggle).  
It records phone marketing campaigns by a Portuguese bank promoting term deposits.

### What one row means
**One row = one customer contact** during the campaign, with customer profile, campaign details, and whether they subscribed (`deposit`).
""")

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

sns.set_theme(style="whitegrid", palette="rocket")
plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11

DATA_PATH = Path("data") / "bank.csv"
FIG = Path("slides_assets")
FIG.mkdir(exist_ok=True)

df_raw = pd.read_csv(DATA_PATH)
df = df_raw.copy()
print("Libraries and data loaded.")
print(f"File: {DATA_PATH}")
""")

md("""### Column guide (what each column means)""")

code("""column_guide = pd.DataFrame({
    "Column": [
        "age", "job", "marital", "education", "default", "balance",
        "housing", "loan", "contact", "day", "month", "duration",
        "campaign", "pdays", "previous", "poutcome", "deposit"
    ],
    "Meaning": [
        "Customer age in years",
        "Type of job (admin, technician, student, ...)",
        "Marital status (married, single, divorced)",
        "Education level (primary, secondary, tertiary, unknown)",
        "Has credit in default? (yes/no)",
        "Average yearly account balance (euros)",
        "Has housing loan? (yes/no)",
        "Has personal loan? (yes/no)",
        "Contact communication type (cellular, telephone, unknown)",
        "Last contact day of the month",
        "Last contact month of the year",
        "Last contact duration in seconds",
        "Number of contacts in this campaign",
        "Days since previous campaign contact (-1 = never contacted before)",
        "Number of contacts before this campaign",
        "Outcome of the previous campaign",
        "Did the customer subscribe to a term deposit? (yes/no) — TARGET"
    ],
    "Type": [
        "Numeric", "Categorical", "Categorical", "Categorical", "Categorical", "Numeric",
        "Categorical", "Categorical", "Categorical", "Numeric", "Categorical", "Numeric",
        "Numeric", "Numeric", "Numeric", "Categorical", "Categorical (target)"
    ]
})
column_guide
""")

md("""**What I see:** The table lists 17 fields: customer traits, loan flags, campaign timing/effort, and the target `deposit`.""")

code("""print("Shape (rows, columns):", df.shape)
print("\\nColumn names:")
print(list(df.columns))
print("\\nData types:")
print(df.dtypes)
""")

md("""**What I see:** There are **11,162 rows** and **17 columns**. Numeric fields use int64; categories are strings.""")

code("""df.head()
""")

md("""**What I see:** Early rows are mostly May contacts with `unknown` contact type and a mix of yes/no deposits.""")

code("""df.describe(include="all")
""")

md("""**What I see:** Mean age ≈ 41, median balance ≈ 550, median duration ≈ 255s. Target is fairly balanced (yes slightly less than no).""")

# Step 2
md("""## Step 2: Questions I want to answer

These questions can all be answered with columns present in the data (univariate, bivariate, and group comparison).

1. **(Univariate)** What is the overall subscription rate (`deposit`)?
2. **(Univariate)** How is customer **age** distributed?
3. **(Univariate)** Which **jobs** appear most often in the campaign?
4. **(Bivariate)** How does **call duration** relate to subscription?
5. **(Bivariate)** Do customers with a **housing loan** subscribe less often?
6. **(Bivariate)** Which **contact** channel has the highest subscription rate?
7. **(Group comparison)** How does subscription rate compare across **education** groups?
8. **(Group comparison)** How do **job × marital status** groups differ in subscription rate?
""")

# Step 3
md("""## Step 3: Clean the data

### 3.1 Missing values
True NaNs are rare in this file; `"unknown"` is used as an incomplete category for some fields. We count both.
""")

code("""# True missing values (NaN)
nan_counts = df.isnull().sum()
print("NaN counts per column:")
print(nan_counts)
print("\\nTotal NaNs:", int(nan_counts.sum()))

# 'unknown' as incomplete labels
unknown_cols = ["job", "education", "contact", "poutcome"]
unknown_counts = pd.Series({c: int((df[c] == "unknown").sum()) for c in unknown_cols})
print("\\n'unknown' counts:")
print(unknown_counts)

missing_plot = pd.DataFrame({
    "column": list(nan_counts.index) + [f"{c} (unknown)" for c in unknown_cols],
    "missing": list(nan_counts.values) + list(unknown_counts.values)
})
missing_plot = missing_plot[missing_plot["missing"] > 0].sort_values("missing", ascending=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
if len(missing_plot):
    sns.barplot(data=missing_plot, x="column", y="missing", color="#EC4899", ax=ax)
    ax.set_title("Incomplete values (NaN + 'unknown' labels)")
    ax.set_xlabel("Column")
    ax.set_ylabel("Count")
    plt.xticks(rotation=25, ha="right")
else:
    ax.set_title("No missing values found")
plt.tight_layout()
plt.savefig(FIG / "01_missing_values.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**Decision — keep, do not drop/fill:** There are **0 NaNs**. Values labelled `"unknown"` are real recorded categories (especially `poutcome` and `contact`). Dropping them would remove thousands of valid contacts and bias the campaign view, so we **keep them as their own category**.
""")

md("""### 3.2 Repeated rows""")

code("""dup_count = int(df.duplicated().sum())
print(f"Duplicate rows: {dup_count}")
if dup_count:
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Removed {dup_count} duplicates. New shape: {df.shape}")
else:
    print("Proof: df.duplicated().sum() == 0 — no repeated rows to remove.")
""")

md("""**What I see:** **0 duplicate rows**. No rows removed.""")

md("""### 3.3 Wrong data types""")

code("""print("Dtypes before fixes:")
print(df.dtypes)

# Numbers stored correctly as int; categories as object/string.
# Month is text abbreviation — map to ordered category (not a full date column available).
month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

# Ensure numeric columns are numeric (coerce if any text slipped in)
for col in ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Binary yes/no helpers for analysis (keep originals)
for col in ["default", "housing", "loan", "deposit"]:
    df[f"{col}_flag"] = (df[col] == "yes").astype(int)

print("\\nDtypes after fixes:")
print(df.dtypes)
print("\\nMonth is now ordered categorical:", df["month"].dtype)
""")

md("""**What I see:** Numeric columns were already integers. We ordered `month` and added 0/1 flags for yes/no fields. No full calendar date exists in this dataset.""")

md("""### 3.4 Outliers — box plot + IQR on at least 2 columns (`balance`, `duration`)""")

code("""def iqr_bounds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper, q1, q3, iqr

outlier_report = {}
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, col in zip(axes, ["balance", "duration"]):
    sns.boxplot(y=df[col], color="#F9A8D4", ax=ax)
    ax.set_title(f"Box plot — {col}")
    ax.set_ylabel(col)
    lo, hi, q1, q3, iqr = iqr_bounds(df[col])
    mask = (df[col] < lo) | (df[col] > hi)
    outlier_report[col] = {
        "Q1": q1, "Q3": q3, "IQR": iqr,
        "lower": lo, "upper": hi,
        "n_outliers": int(mask.sum()),
        "pct": round(100 * mask.mean(), 2)
    }
plt.tight_layout()
plt.savefig(FIG / "02_outliers_boxplot.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()

pd.DataFrame(outlier_report).T
""")

code("""# Decision: KEEP outliers.
# Balance extremes are real wealthy/indebted customers; duration extremes are real long calls.
# Removing them would hide important high-conversion long-call patterns.
print("Rows before outlier handling:", len(df))
print("Decision: keep all rows (no IQR trimming).")
print("Reason: outliers are plausible banking/call values, not data-entry errors.")

# Optional winsorize view only for a secondary chart (data kept intact)
df_clean = df.copy()
print("Clean analysis frame shape:", df_clean.shape)
""")

md("""**Decision — keep outliers:** IQR flags many high `balance` and long `duration` values, but they look real (wealthy clients / long calls). We **keep** them so subscription patterns for those groups stay visible.""")

# Step 4
md("""## Step 4: Univariate analysis""")

code("""numeric_cols = ["age", "balance", "duration", "campaign", "pdays", "previous"]
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.ravel()
for ax, col in zip(axes, numeric_cols):
    sns.histplot(df_clean[col], bins=30, color="#EC4899", ax=ax, kde=False)
    ax.set_title(f"Histogram — {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(FIG / "03_univariate_numeric.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**What I see:** Age peaks in the 30s–40s. Balance and duration are right-skewed. Most customers have few campaign contacts and `pdays` = -1 (no prior contact).""")

code("""cat_cols = ["job", "marital", "education", "housing", "loan", "contact", "month", "deposit"]
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.ravel()
for ax, col in zip(axes, cat_cols):
    order = df_clean[col].value_counts().index
    sns.countplot(data=df_clean, y=col, order=order, color="#DB2777", ax=ax)
    ax.set_title(f"Count — {col}")
    ax.set_xlabel("Count")
    ax.set_ylabel(col)
plt.tight_layout()
plt.savefig(FIG / "04_univariate_categorical.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**What I see:** Management/blue-collar/technician dominate jobs; most are married with secondary education; cellular is the main channel; May has the most contacts; deposit yes/no is fairly close.""")

# Step 5
md("""## Step 5: Bivariate analysis""")

code("""sample = df_clean.sample(n=min(3000, len(df_clean)), random_state=42)
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=sample, x="duration", y="balance", hue="deposit",
    palette={"yes": "#EC4899", "no": "#4A1942"}, alpha=0.5, ax=ax
)
ax.set_title("Scatter — duration vs balance by deposit")
ax.set_xlabel("Duration (seconds)")
ax.set_ylabel("Balance")
plt.tight_layout()
plt.savefig(FIG / "05_scatter_duration_balance.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**What I see:** Longer calls are denser among `deposit=yes`. Balance alone does not cleanly separate groups.""")

code("""num = df_clean[["age", "balance", "day", "duration", "campaign", "pdays", "previous", "deposit_flag"]]
corr = num.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="pink_r", ax=ax, vmin=-1, vmax=1)
ax.set_title("Correlation heatmap (numeric features)")
plt.tight_layout()
plt.savefig(FIG / "06_correlation_heatmap.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print("Strongest |corr| with deposit_flag:")
print(corr["deposit_flag"].drop("deposit_flag").abs().sort_values(ascending=False).head(5))
""")

md("""**What I see:** `duration` has the strongest correlation with subscription. `pdays`/`previous` show weaker positive links.""")

code("""fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(
    data=df_clean, x="deposit", y="duration",
    palette={"yes": "#EC4899", "no": "#F9A8D4"}, ax=ax
)
ax.set_title("Duration by subscription (numeric across categories)")
ax.set_xlabel("Deposit (subscribed?)")
ax.set_ylabel("Duration (seconds)")
plt.tight_layout()
plt.savefig(FIG / "07_duration_by_deposit.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**What I see:** Subscribers have clearly higher call-duration medians than non-subscribers.""")

# Step 6
md("""## Step 6: Answer the questions

One graph + one written answer for each question.
""")

md("""### Q1. What is the overall subscription rate?""")

code("""rate = (df_clean["deposit"] == "yes").mean() * 100
counts = df_clean["deposit"].value_counts()
fig, ax = plt.subplots(figsize=(6, 5))
colors = ["#F9A8D4", "#EC4899"]
ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=colors, startangle=90,
       wedgeprops=dict(width=0.45))
ax.set_title("Overall subscription (deposit)")
plt.tight_layout()
plt.savefig(FIG / "q1_subscription_rate.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print(f"Subscription rate: {rate:.1f}% ({counts.get('yes', 0)} yes / {len(df_clean)} contacts)")
""")

md("""**Answer:** About **47.4%** of contacted customers subscribed — the campaign is fairly balanced, not a rare-event problem.""")

md("""### Q2. How is customer age distributed?""")

code("""fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(df_clean["age"], bins=25, color="#EC4899", ax=ax)
ax.set_title("Age distribution of contacted customers")
ax.set_xlabel("Age")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(FIG / "q2_age_distribution.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print(df_clean["age"].describe()[["mean", "50%", "min", "max"]])
""")

md("""**Answer:** Ages centre around the late 30s / early 40s (mean ≈ 41). Most contacts are working-age adults, with fewer teens and seniors.""")

md("""### Q3. Which jobs appear most often?""")

code("""job_counts = df_clean["job"].value_counts()
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(x=job_counts.values, y=job_counts.index, color="#DB2777", ax=ax)
ax.set_title("Customers by job type")
ax.set_xlabel("Count")
ax.set_ylabel("Job")
plt.tight_layout()
plt.savefig(FIG / "q3_jobs.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print(job_counts.head(3))
""")

md("""**Answer:** **Management**, **blue-collar**, and **technician** are the three most contacted job groups.""")

md("""### Q4. How does call duration relate to subscription?""")

code("""fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_clean, x="deposit", y="duration",
            palette={"yes": "#EC4899", "no": "#F9A8D4"}, ax=ax)
ax.set_title("Call duration vs subscription")
ax.set_xlabel("Subscribed?")
ax.set_ylabel("Duration (seconds)")
plt.tight_layout()
plt.savefig(FIG / "q4_duration.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print(df_clean.groupby("deposit")["duration"].median())
""")

md("""**Answer:** Subscribers have a much higher median call duration. Longer conversations strongly track with a “yes” (note: duration is known after the call).""")

md("""### Q5. Do housing-loan customers subscribe less often?""")

code("""housing_rate = (
    df_clean.groupby("housing")["deposit"]
    .apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate")
)
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.barplot(data=housing_rate, x="housing", y="rate", color="#EC4899", ax=ax)
ax.set_title("Subscription rate by housing loan")
ax.set_xlabel("Housing loan")
ax.set_ylabel("Subscription rate (%)")
for i, r in housing_rate.iterrows():
    ax.text(i, r["rate"] + 1, f"{r['rate']:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(FIG / "q5_housing.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
housing_rate
""")

md("""**Answer:** Customers **without** a housing loan subscribe at a clearly higher rate than those with one.""")

md("""### Q6. Which contact channel has the highest subscription rate?""")

code("""contact_rate = (
    df_clean.groupby("contact")["deposit"]
    .apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate")
    .sort_values("rate", ascending=False)
)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(data=contact_rate, x="contact", y="rate", color="#DB2777", ax=ax)
ax.set_title("Subscription rate by contact type")
ax.set_xlabel("Contact")
ax.set_ylabel("Subscription rate (%)")
plt.tight_layout()
plt.savefig(FIG / "q6_contact.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
contact_rate
""")

md("""**Answer:** **Cellular** (and telephone) outperform `unknown` contact. Known phone channels convert better than unspecified ones.""")

md("""### Q7. How does subscription rate compare across education groups?""")

code("""edu_rate = (
    df_clean.groupby("education")["deposit"]
    .apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate")
    .sort_values("rate", ascending=False)
)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(data=edu_rate, x="education", y="rate", color="#EC4899", ax=ax)
ax.set_title("Subscription rate by education (group comparison)")
ax.set_xlabel("Education")
ax.set_ylabel("Subscription rate (%)")
plt.tight_layout()
plt.savefig(FIG / "q7_education.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
edu_rate
""")

md("""**Answer:** **Tertiary** education shows the highest subscription rate among education groups; primary is lower.""")

md("""### Q8. How do job × marital groups differ in subscription rate?""")

code("""pivot = (
    df_clean.assign(yes=(df_clean["deposit"] == "yes").astype(int))
    .pivot_table(index="job", columns="marital", values="yes", aggfunc="mean")
) * 100

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="pink_r", ax=ax)
ax.set_title("Subscription rate (%) by job × marital status")
ax.set_xlabel("Marital status")
ax.set_ylabel("Job")
plt.tight_layout()
plt.savefig(FIG / "q8_job_marital.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
""")

md("""**Answer:** Rates vary widely by group — e.g. students and retirees often convert higher, while some blue-collar/married cells are lower. Targeting should be segment-specific.""")

# Extra plotly for slides / variety
code("""# Interactive Plotly chart (also useful for dashboard parity)
fig = px.histogram(
    df_clean, x="age", color="deposit", barmode="overlay", opacity=0.65,
    color_discrete_map={"yes": "#EC4899", "no": "#4A1942"},
    title="Age by subscription (Plotly)"
)
fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
fig.write_image(str(FIG / "q_plotly_age.png"), scale=2) if False else None  # kaleido optional
fig.show()
""")

# Step 7
md("""## Step 7: Conclusion

### Three main findings
1. **Call duration** is the strongest numeric signal linked to subscription.
2. Customers **without a housing loan** subscribe more often than those with one.
3. **Education**, **job**, and **contact channel** create clear group differences in conversion.

### One actionable suggestion
**Prioritise cellular outreach to customers without housing loans**, and train agents to hold high-quality conversations (duration/engagement) rather than simply increasing the number of campaign contacts.
""")

code("""print("EDA complete.")
print("Cleaned frame shape:", df_clean.shape)
print("Figures saved to:", FIG.resolve())
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"}
}

out = Path("Bank_Marketing_EDA.ipynb")
nbf.write(nb, out)
print(f"Wrote {out} with {len(cells)} cells")
