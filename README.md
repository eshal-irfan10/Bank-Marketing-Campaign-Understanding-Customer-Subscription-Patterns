# Bank Marketing Campaign — Understanding Customer Subscription Patterns

Exploratory analysis of a bank phone-marketing campaign to learn which customers subscribe to a **term deposit**.

## Live dashboard

> **Streamlit app:** _add your share.streamlit.io URL here after deploy_  
> Example placeholder: `https://YOUR-APP-NAME.streamlit.app`

## Dataset

- **Source:** UCI / Kaggle Bank Marketing dataset  
- **File:** `data/bank.csv`  
- **Size:** 11,162 rows × 17 columns  
- **Target:** `deposit` (`yes` / `no`)

## Project contents

| File / folder | Purpose |
|---|---|
| `Bank_Marketing_EDA.ipynb` | Full EDA notebook (Part 2) |
| `app.py` | Streamlit dashboard (Part 3) |
| `data/bank.csv` | Dataset |
| `slides_assets/` | Chart images for Google Slides |
| `SLIDES_GUIDE.md` | Slide-by-slide Google Slides outline |
| `requirements.txt` | Python dependencies |

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

The dashboard uses a pink / magenta / plum theme (see `.streamlit/config.toml` and custom CSS in `app.py`).

Open the notebook with Jupyter / VS Code / Google Colab (upload `data/bank.csv` next to the notebook or keep the `data/` relative path).

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (public).  
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.  
3. Select the repo, branch `main`, main file `app.py`.  
4. Deploy, then paste the live URL into this README and into Slide 13.

## Main findings

1. Longer call **duration** strongly tracks with subscription.  
2. Customers **without a housing loan** subscribe more often.  
3. **Job, education, and contact channel** create clear conversion gaps.

**Suggestion:** Prioritise cellular outreach to customers without housing loans and invest in call quality over extra contact attempts.
