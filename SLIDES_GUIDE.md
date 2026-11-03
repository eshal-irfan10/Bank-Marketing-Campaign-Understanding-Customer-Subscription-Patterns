# Google Slides Guide (Part 4)

Create a **new Google Slides** deck (File → New → Google Slides).  
Use theme colours: **Plum `#4A1942`**, **Pink `#EC4899`**, **Soft pink `#F9A8D4`**, white background.  
Fonts: headings ≥ 36, body ≥ 24. Max ~25 words per slide.

Insert charts from the `slides_assets/` folder (Upload → Image).

Share → General access → **Anyone with the link** → **Viewer**.

---

## Slide 1 — Title
- Project: Bank Marketing Campaign — Customer Subscription Patterns  
- Your name · 3 Nov 2026  
- Insert a bank / marketing image (Unsplash or similar)

## Slide 2 — Introduction
- Chose bank marketing data to study real campaign outcomes  
- Big question: **Who subscribes to a term deposit after a call?**

## Slide 3 — Dataset details (3 big number boxes)
- **11,162** rows  
- **17** columns  
- **UCI / Kaggle** Bank Marketing (phone campaign; months across the year)

## Slide 4 — Column guide
Small table (from notebook): age, job, balance, housing, contact, duration, campaign, poutcome, **deposit (target)**

## Slide 5 — Questions
List Q1–Q8 from the notebook (short lines).

## Slide 6 — Cleaning: missing values
- Image: `slides_assets/01_missing_values.png`  
- Headline: **0 NaNs — kept “unknown” as its own category**

## Slide 7 — Cleaning: duplicates & types
- Big number: **0 repeated rows**  
- Line: Month ordered; yes/no flags added; numerics already correct

## Slide 8 — Outliers
- Image: `slides_assets/02_outliers_boxplot.png`  
- Headline: **Kept balance & duration outliers — real customers, real long calls**

## Slide 9 — Univariate
- Images: `03_univariate_numeric.png` + `q2_age_distribution.png` (or `q3_jobs.png`)  
- Lines: Age peaks 30–40 · Management / blue-collar / technician dominate

## Slide 10 — Bivariate
- Images: `05_scatter_duration_balance.png` + `06_correlation_heatmap.png`  
- Headline: **Strongest link: call duration ↔ subscription**

## Slide 11 — Key finding 1
- Image: `finding1_duration.png`  
- Headline: **Longer calls strongly track with “yes”**

## Slide 12 — Key finding 2
- Image: `finding2_housing.png`  
- Headline: **No housing loan → higher subscription rate**

## Slide 13 — Dashboard
- Screenshot your live Streamlit app  
- Paste the share.streamlit.io link (and optional QR)

## Slide 14 — Conclusion & suggestion
- 3 findings: duration · housing loan · job/education/contact segments  
- Action: **Prioritise cellular outreach to customers without housing loans**

## Slide 15 — Thank you
- GitHub repo link  
- “Questions?”

---

After deploying Streamlit, put the live URL in `README.md` and on Slide 13.
