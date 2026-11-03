"""Execute EDA analysis non-interactively and save slide figures."""
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (9, 5)

DATA_PATH = Path("data") / "bank.csv"
FIG = Path("slides_assets")
FIG.mkdir(exist_ok=True)

df_raw = pd.read_csv(DATA_PATH)
df = df_raw.copy()

# Missing / unknown plot
nan_counts = df.isnull().sum()
unknown_cols = ["job", "education", "contact", "poutcome"]
unknown_counts = pd.Series({c: int((df[c] == "unknown").sum()) for c in unknown_cols})
missing_plot = pd.DataFrame({
    "column": list(nan_counts.index) + [f"{c} (unknown)" for c in unknown_cols],
    "missing": list(nan_counts.values) + list(unknown_counts.values)
})
missing_plot = missing_plot[missing_plot["missing"] > 0].sort_values("missing", ascending=False)
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(data=missing_plot, x="column", y="missing", color="#EC4899", ax=ax)
ax.set_title("Incomplete values (NaN + 'unknown' labels)")
ax.set_xlabel("Column"); ax.set_ylabel("Count")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(FIG / "01_missing_values.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Dtypes / month
month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)
for col in ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
for col in ["default", "housing", "loan", "deposit"]:
    df[f"{col}_flag"] = (df[col] == "yes").astype(int)

# Outliers boxplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, col in zip(axes, ["balance", "duration"]):
    sns.boxplot(y=df[col], color="#F9A8D4", ax=ax)
    ax.set_title(f"Box plot — {col}")
    ax.set_ylabel(col)
plt.tight_layout()
plt.savefig(FIG / "02_outliers_boxplot.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

df_clean = df.copy()

# Univariate numeric
numeric_cols = ["age", "balance", "duration", "campaign", "pdays", "previous"]
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
for ax, col in zip(axes.ravel(), numeric_cols):
    sns.histplot(df_clean[col], bins=30, color="#EC4899", ax=ax)
    ax.set_title(f"Histogram — {col}")
plt.tight_layout()
plt.savefig(FIG / "03_univariate_numeric.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Univariate categorical
cat_cols = ["job", "marital", "education", "housing", "loan", "contact", "month", "deposit"]
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
for ax, col in zip(axes.ravel(), cat_cols):
    order = df_clean[col].value_counts().index
    sns.countplot(data=df_clean, y=col, order=order, color="#DB2777", ax=ax)
    ax.set_title(f"Count — {col}")
plt.tight_layout()
plt.savefig(FIG / "04_univariate_categorical.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Scatter
sample = df_clean.sample(n=min(3000, len(df_clean)), random_state=42)
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=sample, x="duration", y="balance", hue="deposit",
                palette={"yes": "#EC4899", "no": "#4A1942"}, alpha=0.5, ax=ax)
ax.set_title("Scatter — duration vs balance by deposit")
plt.tight_layout()
plt.savefig(FIG / "05_scatter_duration_balance.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Heatmap
num = df_clean[["age", "balance", "day", "duration", "campaign", "pdays", "previous", "deposit_flag"]]
corr = num.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="pink_r", ax=ax, vmin=-1, vmax=1)
ax.set_title("Correlation heatmap (numeric features)")
plt.tight_layout()
plt.savefig(FIG / "06_correlation_heatmap.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Duration by deposit
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_clean, x="deposit", y="duration",
            palette={"yes": "#EC4899", "no": "#F9A8D4"}, ax=ax)
ax.set_title("Duration by subscription")
plt.tight_layout()
plt.savefig(FIG / "07_duration_by_deposit.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Q charts
rate = (df_clean["deposit"] == "yes").mean() * 100
counts = df_clean["deposit"].value_counts()
fig, ax = plt.subplots(figsize=(6, 5))
ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#F9A8D4", "#EC4899"],
       startangle=90, wedgeprops=dict(width=0.45))
ax.set_title("Overall subscription (deposit)")
plt.tight_layout()
plt.savefig(FIG / "q1_subscription_rate.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(df_clean["age"], bins=25, color="#EC4899", ax=ax)
ax.set_title("Age distribution of contacted customers")
plt.tight_layout()
plt.savefig(FIG / "q2_age_distribution.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

job_counts = df_clean["job"].value_counts()
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(x=job_counts.values, y=job_counts.index, color="#DB2777", ax=ax)
ax.set_title("Customers by job type")
plt.tight_layout()
plt.savefig(FIG / "q3_jobs.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_clean, x="deposit", y="duration",
            palette={"yes": "#EC4899", "no": "#F9A8D4"}, ax=ax)
ax.set_title("Call duration vs subscription")
plt.tight_layout()
plt.savefig(FIG / "q4_duration.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

housing_rate = (
    df_clean.groupby("housing")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate")
)
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.barplot(data=housing_rate, x="housing", y="rate", color="#EC4899", ax=ax)
ax.set_title("Subscription rate by housing loan")
plt.tight_layout()
plt.savefig(FIG / "q5_housing.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

contact_rate = (
    df_clean.groupby("contact")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate").sort_values("rate", ascending=False)
)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(data=contact_rate, x="contact", y="rate", color="#DB2777", ax=ax)
ax.set_title("Subscription rate by contact type")
plt.tight_layout()
plt.savefig(FIG / "q6_contact.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

edu_rate = (
    df_clean.groupby("education")["deposit"].apply(lambda s: (s == "yes").mean() * 100)
    .reset_index(name="rate").sort_values("rate", ascending=False)
)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(data=edu_rate, x="education", y="rate", color="#EC4899", ax=ax)
ax.set_title("Subscription rate by education")
plt.tight_layout()
plt.savefig(FIG / "q7_education.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

pivot = (
    df_clean.assign(yes=(df_clean["deposit"] == "yes").astype(int))
    .pivot_table(index="job", columns="marital", values="yes", aggfunc="mean")
) * 100
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="pink_r", ax=ax)
ax.set_title("Subscription rate (%) by job × marital status")
plt.tight_layout()
plt.savefig(FIG / "q8_job_marital.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

# Extra finding slides
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_clean, x="deposit", y="duration",
            palette={"yes": "#EC4899", "no": "#F9A8D4"}, ax=ax)
ax.set_title("Finding: Longer calls → more subscriptions")
plt.tight_layout()
plt.savefig(FIG / "finding1_duration.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

fig, ax = plt.subplots(figsize=(6, 4.5))
sns.barplot(data=housing_rate, x="housing", y="rate", color="#EC4899", ax=ax)
ax.set_title("Finding: No housing loan → higher yes rate")
for i, r in housing_rate.iterrows():
    ax.text(i, r["rate"] + 1, f"{r['rate']:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(FIG / "finding2_housing.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()

print("Subscription rate:", round(rate, 2))
print("Duplicates:", int(df_raw.duplicated().sum()))
print("NaNs:", int(df_raw.isnull().sum().sum()))
print("Housing rates:")
print(housing_rate)
print("Duration medians:")
print(df_clean.groupby("deposit")["duration"].median())
print("Saved figures:", sorted(p.name for p in FIG.glob("*.png")))
