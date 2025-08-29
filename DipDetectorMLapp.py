# app.py
import os, pandas as pd, joblib, streamlit as st
from core import fetch_snapshot, load_state, save_state, tiers_to_send, format_alert_email, send_email

st.set_page_config(page_title="BTC Dips — Live & ML", layout="centered")
st.title("BTC Dip Alerts — Live & ML")

tab_live, tab_ml = st.tabs(["📉 Live Monitor", "🧠 ML Prediction"])

# ---- LIVE MONITOR ----
with tab_live:
    snap = fetch_snapshot()
    c1, c2, c3 = st.columns(3)
    c1.metric("Price (USD)", f"${snap['price']:,.2f}")
    c2.metric("24h Change", f"{snap['pct24']:.2f}%")
    c3.metric("24h Range", f"${snap['low24']:.0f} — ${snap['high24']:,.0f}")
    st.caption(f"Updated: {snap['ts']}")

    # Simulator for testing (teacher can see you tested!)
    sim = st.slider("Simulate 24h % change (testing only)", -30.0, 30.0, value=None, step=0.1, format="%.1f")
    if sim is not None:
        snap["pct24"] = float(sim)
        st.info(f"Simulating pct24 = {sim:.2f}%")

    state = load_state()
    st.write("Already alerted tiers (today):", state.get("sent_tiers", []))

    to_send = tiers_to_send(snap["pct24"], state.get("sent_tiers", []))
    if to_send:
        st.warning(f"Tier {to_send[0]:.0f}% JUST hit (24h change {snap['pct24']:.2f}%).")

    colA, colB = st.columns(2)
    if colA.button("Send test email"):
        subj, html, text = format_alert_email(snap, tier=0.0, ml_note=None)
        try:
            send_email("[TEST] " + subj, html, text)
            st.success("Test email sent.")
        except Exception as e:
            st.error(f"Email error: {e}")

    if to_send and colB.button(f"Send real alert ({to_send[0]:.0f}%)"):
        t = to_send[0]
        subj, html, text = format_alert_email(snap, tier=t, ml_note=None)
        try:
            send_email(subj, html, text)
            state.setdefault("sent_tiers", []).append(t)
            state.setdefault("log", []).append({"ts": snap["ts"], "tier": t, "pct24": snap["pct24"], "price": snap["price"]})
            state["last_price"] = snap["price"]
            save_state(state)
            st.success("Alert sent and state updated.")
        except Exception as e:
            st.error(f"Email error: {e}")

    st.subheader("Alert log")
    log = state.get("log", [])
    if log:
        st.dataframe(pd.DataFrame(log))
    else:
        st.write("No alerts yet.")

# ---- ML PREDICTION (works with Mohammed model) ----
with tab_ml:
    st.write("Loads `dip20_model.joblib` if present (serialized sklearn Pipeline).")
    if not os.path.exists("dip20_model.joblib"):
        st.info("Model file not found. Ask Mohammed to export `dip20_model.joblib` with `pipeline` + `features`.")
    else:
        try:
            bundle = joblib.load("dip20_model.joblib")
            pipe = bundle["pipeline"]; FEATURES = bundle["features"]
            snap = fetch_snapshot()
            feat = {
                "current_price": snap["price"],
                "market_cap": snap["mcap"],
                "total_volume": snap["vol"],
                "price_change_percentage_24h": snap["pct24"],
                "high_24h": snap["high24"],
                "low_24h": snap["low24"],
            }
            missing = [c for c in FEATURES if c not in feat]
            if missing:
                st.error(f"Missing features for inference: {missing}")
            else:
                X = pd.DataFrame([{k: feat[k] for k in FEATURES}])
                proba = float(pipe.predict_proba(X)[0,1])
                st.metric("P(≥20% dip in window)", f"{proba:.0%}")
                if st.button("Send alert with ML note"):
                    subj, html, text = format_alert_email(snap, tier=0.0, ml_note=proba)
                    send_email("[ML NOTE] " + subj, html, text)
                    st.success("Email sent with ML probability.")
        except Exception as e:
            st.error(f"Inference error: {e}")
