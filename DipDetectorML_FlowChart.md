```Mermaid
flowchart LR
  %% ====== LAYERS ======
  subgraph U[👥 Users]
    U1[Subscribe / Set Preferences\n(email, thresholds 2/5/10/15/20)]
  end

  subgraph ING[🌐 Live Data Ingest]
    I1[Fetch BTC price\n(CoinGecko API)]
    I2[Compute % change\n(24h / 7d windows)]
  end

  subgraph AE[🧠 Alert Engine]
    A1{Dip ≥ threshold?}
    A2[Log check\n(data/price_log.csv)]
  end

  subgraph ML[🤖 ML Pipeline]
    M1[Load historical BTC CSV]
    M2[Feature engineering\n(returns, RSI, volatility, volume)]
    M3[Train Random Forest]
    M4[Evaluate & metrics\n(reports/metrics.txt)]
    M5[Monthly forecast]
    M6[[Write artifact\n data/ml_monthly_prob.json]]
  end

  subgraph EM[✉️ Email Delivery]
    E1[Build email (HTML)]
    E2{Delivery channel}
    E3[SMTP (demo)]
    E4[AWS SES (future)]
  end

  subgraph UI[🖥️ Dashboard]
    D1[Read live snapshot]
    D2[Read monthly_dip_prob\n(data/ml_monthly_prob.json)]
    D3[Render Streamlit UI\n(app.py)]
    D4[Show email preview &\nthreshold status]
    D5[Visuals: price line &\ndip thresholds]
  end

  subgraph DS[(🗂️ Data Stores)]
    S1[(data/price_log.csv)]
    S2[(data/ml_monthly_prob.json)]
    S3[(models/rf_monthly.pkl)]
    S4[(reports/metrics.txt)]
  end

  %% ====== FLOWS ======
  %% User prefs to UI
  U1 -->|prefs (threshold, email)| D3

  %% Live ingest → alert engine → logs
  I1 --> I2 --> A1 --> A2 --> S1
  A1 -- Yes --> E1
  A1 -- No  --> D1

  %% Email delivery branch
  E1 --> E2
  E2 -- SMTP --> E3 -->|send| U1
  E2 -- SES  --> E4 -. future .-> U1

  %% ML path
  M1 --> M2 --> M3 --> M4 --> M5 --> M6 --> S2
  M3 --> S3

  %% Dashboard reads from stores
  S1 --> D1
  S2 --> D2
  D1 --> D3
  D2 --> D3
  D3 --> D4
  D3 --> D5

  %% Styling
  classDef store fill:#f3f4f6,stroke:#9ca3af,color:#111,stroke-width:1px;
  class S1,S2,S3,S4 store;
