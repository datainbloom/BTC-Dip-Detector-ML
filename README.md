# BTC-Dip-Detector-ML

## :money_with_wings: Dip Detector ML :rotating_light:
Welcome to the BTC Dip Detector project! This machine learning repository is built to detect significant dips in Bitcoin prices using historical data, statistical indicators, and classification models. This project is being developed as part of The Knowledge House 2025 Data Science Fellowship.
**Team Name:** Wave Riders :ocean:
**Team Members:**
- Jessenia (Lead)
- Kachi
- Mohammed
- Rosania
- Belkis
---
**DipDetectorML** is a hybrid **system** that combines:
1) :zap: **Rule-based live alerts** – monitors Bitcoin (BTC) in real time and emails users when dips of **2%, 5%, 10%, 15%, or 20%** occur.
2) :busts_in_silhouette: **Machine learning forecasting** – trains a **Random Forest model** on historical BTC data to predict the probability of a **≥20% monthly dip** and sends a monthly warning email if risk is high.
It’s designed for **long-term Bitcoin accumulators** who never sell—only buy “as mucho and as often as possible.” By layering real-time alerts with predictive foresight, DipDetectorML helps users **supercharge their Dollar Cost Averaging (DCA) strategy**, stacking more BTC at better prices.
---
## :dart: Motivation
Bitcoin is one of the most volatile assets in modern finance:
- :chart_with_downwards_trend: **Daily or weekly dips of ~10–20%** can occur during volatile periods.
- :bar_chart: Even in bull markets, **~20–27% corrections** are common “healthy pullbacks.”
- :date: In Feb 2025, BTC saw a **~17% monthly drop**.
- :bear: Full bear markets can bring **50–80% drawdowns**.
Static **buy orders** in exchange apps are tied to fixed prices, quickly go stale as BTC trends, and provide **no foresight**.
**DipDetectorML is different**: alerts are **percentage-based** (adaptive at any price) and we also provide a **predictive monthly risk signal**. It’s built for accumulators who DCA steadily but **size up on deep dips** and **plan liquidity ahead of downturns**.
This project is also a **real-world ML case study**:
- :broom: Data collection/cleaning from crypto APIs
- :hammer_and_wrench: Feature engineering (returns, volatility, RSI-14, log(volume))
- :brain: Model training with class imbalance
- :mailbox_with_mail: Deployment: live polling, CSV logging, multi-recipient email
---
## :blue_book: Project Overview
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
## :white_check_mark: Results & Evaluation (MVP Checkpoint)
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
## :bulb: Value Proposition
DipDetectorML is a **smarter accumulation assistant** for long-term holders:
- :arrows_counterclockwise: **Better than static buy orders:** static limit prices go stale; **percent-based** alerts adapt at any price level.
- :compass: **Control + discipline:** we notify; you decide sizing. Example rule-set:
  - 5% dip → advance weekly DCA
  - 10% dip → 2× DCA
  - 20% dip → 3× DCA
- :crystal_ball: **Predictive foresight:** the monthly crash forecast helps you **stage cash** ahead of major downturns rather than reacting late.
---
## :warning: Limitations
- :speech_balloon: **Class imbalance:** true ≥20% dips are rare; requires careful thresholding and metrics.
- :hourglass_flowing_sand: **Non-stationarity:** crypto regimes change; models can drift.
- :lock: **API rate limits:** CoinGecko free tier is 100k requests/month → poll responsibly.
- :dart: **Scope:** MVP focuses on BTC; multi-asset remains future work.
- :e-mail: **Email delivery:** SMTP configuration still being finalized.
---
## :pray: Acknowledgments & Team Contributions 
### :busts_in_silhouette: Team Contributions
- **Jessenia (Lead):** :star2: Slack + GitHub setup, README, standups, documentation, demo coordination, final submission.
- **Kachi:** :zap: Built live API polling + dip logic, CSV logging; actively integrating SMTP for email delivery.
- **Mohammed:** :bust_in_silhouette: Implemented **RandomForestClassifier**, engineered features, ran **Grid/RandomizedSearchCV**, produced **AUC/precision/recall**, **confusion matrix**, and saved the model with `joblib`.
- **Rosania:** :memo: Drafted documentation and background research.
- **Belkis:** :email: Worked on email integration.
### :raised_hands: Special Acknowledgments
- **Maurice** (Mentor) :bulb: — for guidance, review, and support throughout the project.
- **Farouk** (Instructor) :mortar_board: — for technical instruction and ML insights.
- **Gaurav** (Instructor) :mortar_board: — for teaching, feedback, and continued support.
Special thanks also to **CoinGecko** :lizard: for providing free API access that made the live alert system possible.
---
## :scroll: License
MIT License.
CoinGecko API data subject to their terms of service: https://www.coingecko.com/en/terms
---
We welcome input and insights! Please fork, clone, and submit PRs.
---

## :chart_with_upwards_trend: Dip Detector ML Demo (Screenshots and Video)

<img width="997" height="371" alt="image (5)" src="https://github.com/user-attachments/assets/18474602-d27e-4c55-87a8-4f9994333b69" />
<br>

<img width="1366" height="890" alt="image (1)" src="https://github.com/user-attachments/assets/70c8a790-e919-4d6f-84a0-f4a95e787c55" />  <br>

<img width="1250" height="892" alt="image (2)" src="https://github.com/user-attachments/assets/a6b2c7bf-9483-48e8-a83a-aa40978388c2" />  <br>

<img width="1251" height="889" alt="image (3)" src="https://github.com/user-attachments/assets/dfd612b2-a99b-4c32-a11a-3437ddfe35ec" />  <br>

<img width="1092" height="900" alt="image (4)" src="https://github.com/user-attachments/assets/65715876-f3a5-4fa2-af96-9ae8045b23b2" />  <br>

[![IMAGE ALT TEXT](http://img.youtube.com/vi/8eToJtgs0P0/0.jpg)](http://www.youtube.com/watch?v=8eToJtgs0P0 "Dip Detector ML Demo")


