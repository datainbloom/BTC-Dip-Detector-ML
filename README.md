 ## 💸 Dip Detector ML 🚨

Welcome to the BTC Dip Detector project! This machine learning repository is built to detect significant dips in Bitcoin prices using historical data, statistical indicators, and classification models. This project is being developed as part of The Knowledge House 2025 Data Science Fellowship.

---

<p align="center">
  <img src="Images\DipDetectorML_Architectural_Flowchart.png" alt="Dip Detector ML Flowchart", width="70%">
  <br/>
  <em>This diagram shows how DipDetectorML fetches live Bitcoin data, checks for price dips, runs a machine learning forecast, and then delivers alerts and dashboard updates to the user</em>
</p>

---

**Team Name:** Wave Riders 🌊  
**Team Members:**  
- Jessenia (Lead)  
- Kachi  
- Mohammed  
- Rosania  
- Belkis  

---

**DipDetectorML** is a hybrid **system** that combines:  
1) ⚡ **Rule-based live alerts** – monitors Bitcoin (BTC) in real time and emails users when dips of **2%, 5%, 10%, 15%, or 20%** occur.  
2) 🤖 **Machine learning forecasting** – trains a **Random Forest model** on historical BTC data to predict the probability of a **≥20% monthly dip** and sends a monthly warning email if risk is high.  

It’s designed for **long-term Bitcoin accumulators** who never sell—only buy “as mucho and as often as possible.” By layering real-time alerts with predictive foresight, DipDetectorML helps users **supercharge their Dollar Cost Averaging (DCA) strategy**, stacking more BTC at better prices.  

---

## 🎯 Motivation

Bitcoin is one of the most volatile assets in modern finance:  
- 📉 **Daily or weekly dips of ~10–20%** can occur during volatile periods.  
- 📊 Even in bull markets, **~20–27% corrections** are common “healthy pullbacks.”  
- 📅 In Feb 2025, BTC saw a **~17% monthly drop**.  
- 🐻 Full bear markets can bring **50–80% drawdowns**.

Static **buy orders** in exchange apps are tied to fixed prices, quickly go stale as BTC trends, and provide **no foresight**.  
**DipDetectorML is different**: alerts are **percentage-based** (adaptive at any price) and we also provide a **predictive monthly risk signal**. It’s built for accumulators who DCA steadily but **size up on deep dips** and **plan liquidity ahead of downturns**.

This project is also a **real-world ML case study**:  
- 🧹 Data collection/cleaning from crypto APIs  
- 🛠️ Feature engineering (returns, volatility, RSI-14, log (volume))  
- 🧠 Model training with class imbalance  
- 📬 Deployment: live polling, CSV logging, multi-recipient email  

---

## 📘 Project Overview

**End-to-end system for monitoring and predicting BTC dips:**

1) **Live dip alerts**  
   - Polls CoinGecko `/coins/markets` every 60s  
   - Checks 24h & 7d % changes vs thresholds (2/5/10/15/20)  
   - Appends each sample to `data/live_btc_log.csv` (proof + charts)  
   - Emails all subscribers whose preferences match the dip  

2) **Historical training + ML forecast**  
   - Pulls daily OHLC + volume via `/market_chart`  
   - Features: 1/3/7-day returns, rolling vol (7/14d), RSI-14, log(volume)  
   - Trains **RandomForestClassifier** to predict a **≥20%** next-month dip risk  
   - Saves model to `models/rf_monthly.pkl`  
   - Runs monthly to send **one** “high-risk” forecast email  

---

## 👥 Users
Primary users are:  
- Retail crypto investors and long-term accumulators.  
- Students and analysts learning applied machine learning on financial time-series.  
- Educators and instructors reviewing our project for technical rigor.  

They want:  
- 📧 Clear, reliable email alerts.  
- 📊 Simple visuals and dashboards.  
- 🔮 Actionable insights (probabilities, not just thresholds).  

---

## ⚙️ Setup Instructions
Clone the repo and set up dependencies:

```bash
git clone https://github.com/your-username/DipDetectorML.git
cd DipDetectorML

python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## 🗂️ Code Structure

```
BTC-DipDetector-ML/
│
├── Data/
│   └── bitcoin_cleaned_with_features.csv
│
├── files/
│   ├── dip_detector_model.pkl
│   ├── feature_list.pkl
│   └── monthly_forecast.py
│
├── Images/
│   └── DipDetectorML_Architectural_Flowchart.png
│
├── Notebooks/
│   ├── Belkis.ipynb
│   ├── Jessenia.ipynb
│   ├── ML_Random_Forest_Mohammed.ipynb
│   ├── Onyekachi.ipynb
│   └── Rosania.ipynb
│
├── DipDetectorML_FlowChart.md
├── DipDetectorMLapp.py
├── core.py
├── requirements.txt
├── README.md
└── .env

```

---

## 📑 Data Sources

Live BTC prices: CoinGecko API 🦎

Historical CSV: cached from CoinGecko’s /market_chart endpoint

Model outputs: /data/ml_monthly_prob.json

---

## 🧪 Testing Data

We’ll build a 20-example test set covering:

Easy: clear 20% dips (label = 1).

Medium: borderline dips (10–19% changes).

Hard: false positives (volatile days that recover).

Out-of-scope: sideways markets with no significant dips.

Correctness defined by: model’s probability alignment with true label (≥0.5 = dip, else no dip), plus evaluation on AUC and precision/recall.

---

## 🛠 📦 Dependencies and Tools

Key libraries used in this project:

pandas, numpy → data wrangling

requests → API calls (CoinGecko)

scikit-learn, joblib → ML (Random Forest)

matplotlib, seaborn, plotly → visualization

streamlit → dashboard demo

boto3, python-dotenv → (future SES integration)

See requirements.txt for full list.

Scikit-learn: Logistic Regression, Random Forest (main ML).

XGBoost / LightGBM: optional boosted-tree experiments.

(Stretch) TensorFlow/Keras for LSTM.

Requests / Pandas: API ingestion and data wrangling.

Matplotlib / Seaborn: visualization.

SMTP integration: alerts/notifications.

---

## 📊 Metrics (Mohammed’s Outputs)

The Random Forest classifier was trained on BTC daily OHLC + features like lagged returns, RSI, and volatility.

AUC: 0.74

Precision: 0.68

Recall: 0.55

Confusion Matrix + Classification Report: included in /reports/metrics.txt.

Example test row outputs include:

Date

Engineered features

Predicted probability

Actual next-day return

Label (dip / no dip)

---

## ✅ Results & Evaluation (MVP Checkpoint)

### Working Prototype
- **Live alerts:** System polls CoinGecko and triggers emails on threshold breach. (For demo we temporarily set a tiny threshold, e.g., **−0.1%**, to force an alert and prove delivery.)  
- **Random Forest model:** Trains on cached CSV of historical BTC features; outputs a probability of a **≥20% monthly dip**.  

### Evaluation
- Notebook includes **10–20 test rows** with: date, engineered features, predicted probability, actual next-day return, and label (dip/no dip).  
- Report **AUC** and **precision/recall** at the chosen probability cutoff.  
- Include **confusion matrix** and **classification report** (Mohammed’s code).  

### Current Status of Email
- SMTP wiring is **in progress** (Kachi). Alerts trigger correctly; configuring credentials/routes for reliable inbox delivery is the remaining step.  

---

## 💡 Value Proposition

DipDetectorML is a **smarter accumulation assistant** for long-term holders:

Provides immediate situational awareness (rule-based alerts).

Adds predictive foresight for portfolio risk management (ML monthly forecast).

Educationally, demonstrates both classical ML (Random Forest, Logistic Regression) and time-series approaches (possible LSTM as a stretch goal).

- 🔄 **Better than static buy orders:** static limit prices go stale; **percent-based** alerts adapt at any price level.  
- 🧭 **Control + discipline:** we notify; you decide sizing. Example rule-set:  
  - 5% dip → advance weekly DCA  
  - 10% dip → 2× DCA  
  - 20% dip → 3× DCA  
- 🔮 **Predictive foresight:** the monthly crash forecast helps you **stage cash** ahead of major downturns rather than reacting late.  

---

## ⚠️ Limitations

- ⚖️ **Class imbalance:** true ≥20% dips are rare; requires careful thresholding and metrics.  
- ⏳ **Non-stationarity:** crypto regimes change; models can drift.  
- 🔒 **API rate limits:** CoinGecko free tier is 100k requests/month → poll responsibly.  
- 🎯 **Scope:** MVP focuses on BTC; multi-asset remains future work.  
- 📧 **Email delivery:** SMTP configuration still being finalized.  

---

## ✅ Solutions to Risks

Address imbalance with class_weight="balanced" in Random Forest/LogReg.

Consider expanding dataset to include multiple coins (ETH, XRP) for training, even if evaluation is BTC-only.

Keep LSTM/GRU as a stretch goal; Random Forest = main deliverable.

Allow flexible thresholds for rule-based alerts to balance alert frequency.

---

## 🔮 Future Work

- 📈 Backtests: compare **DCA-only** vs **DCA + DipDetectorML** over 1–3 years (extra BTC stacked).  
- 🌍 Add ETH, XRP, and others; cross-asset signals.  
- 📰 Add news/sentiment features (Fed/CPI, ETF flows, exchange events).  
- 🚀 Model upgrades: XGBoost/LightGBM; sequence models (LSTM/GRU).  
- 📲 Slack bot or mobile push as alternatives to email.  
- 👥 User preferences: per-user tiers, unsubscribe links, dashboards.  
- ☁️ AWS SES + DynamoDB for production alerts.

---

## 🙏 Acknowledgments & Team Contributions  

### 👥 Team Contributions
- **Jessenia (Lead):** 🌟 Slack + GitHub setup, README, standups, documentation, demo coordination, final submission.  
- **Onyekachi:** ⚡ Built live API polling + dip logic, CSV logging; actively integrating SMTP for email delivery.  
- **Mohammed:** 🤖 Implemented **RandomForestClassifier**, engineered features, ran **Grid/RandomizedSearchCV**, produced **AUC/precision/recall**, **confusion matrix**, and saved the model with `joblib`.  
- **Rosania:** 📝 Drafted documentation and background research.  
- **Belkis:** ✉️ Email intergration collaboration.

### 🙌 Special Acknowledgments
- **Maurice** (Mentor) 💡 — for constructive guidance, review, and unwavering support throughout the project.  
- **Farukh** (Instructor) 🎓 — for technical instruction, ML insight and insightful feedback.  
- **Gaurav** (Instructor) 🎓 — for teaching, feedback, and continued assistance.  

Special thanks also to **CoinGecko** 🦎 for providing free API access that made the live alert system possible.  

---

## 📜 License
MIT License.  
CoinGecko API data subject to their terms of service: https://www.coingecko.com/en/terms 



