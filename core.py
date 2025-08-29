# core.py
import os, ssl, smtplib, json, requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"
STATE_FP = Path("dip_state.json")
TIERS = [-2.0, -5.0, -10.0, -15.0, -20.0]  # percentages (negative = dip)

load_dotenv(find_dotenv())
EMAIL_SENDER = os.getenv("EMAIL_SENDER") or ""
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") or ""
EMAIL_RECIPIENTS = [e.strip() for e in os.getenv("EMAIL_RECIPIENTS","").split(",") if e.strip()]

def fetch_snapshot():
    """Return a dict of current BTC stats pulled from CoinGecko."""
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    row = r.json()[0]
    return {
        "name": row["name"],
        "price": float(row["current_price"]),
        "pct24": float(row["price_change_percentage_24h"] or 0.0),  # e.g. -0.53 means -0.53%
        "high24": float(row["high_24h"]),
        "low24": float(row["low_24h"]),
        "mcap": float(row["market_cap"]),
        "vol": float(row["total_volume"]),
        "ts": datetime.utcnow().isoformat() + "Z",
    }

def load_state():
    if STATE_FP.exists():
        try: return json.loads(STATE_FP.read_text())
        except: pass
    return {"last_price": None, "sent_tiers": [], "log": []}

def save_state(state):
    STATE_FP.write_text(json.dumps(state, indent=2))

def tiers_to_send(pct24, sent):
    """Return the deepest new tier crossed (list of length 0 or 1)."""
    pending = [t for t in TIERS if pct24 <= t and t not in sent]
    return pending[-1:] if pending else []

def send_email(subject, html_body, text_body="See HTML"):
    if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECIPIENTS):
        raise RuntimeError("Email env not configured")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
        s.login(EMAIL_SENDER, EMAIL_PASSWORD)
        s.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())

def format_alert_email(snap, tier, ml_note=None):
    """Return (subject, html, text) for the alert email."""
    subject = f"BTC dip alert: {snap['pct24']:.2f}% (hit {tier:.0f}% tier) — ${snap['price']:,.2f}"
    extra = f"<p><b>ML P(≥20% dip):</b> {ml_note:.0%}</p>" if ml_note is not None else ""
    html = f"""
    <h2>BTC dipped {snap['pct24']:.2f}% in 24h</h2>
    <p><b>Price:</b> ${snap['price']:,.2f}<br>
       <b>24h High:</b> ${snap['high24']:,.2f}<br>
       <b>24h Low:</b> ${snap['low24']:,.2f}<br>
       <b>Market Cap:</b> ${snap['mcap']:,.0f}<br>
       <b>Volume:</b> ${snap['vol']:,.0f}</p>
    {extra}
    <p><i>{snap['ts']}</i></p>
    """
    text = (
        f"BTC dipped {snap['pct24']:.2f}% in 24h\n"
        f"Price: ${snap['price']:,.2f}\n"
        f"24h High: ${snap['high24']:,.2f}\n"
        f"24h Low: ${snap['low24']:,.2f}\n"
        f"Market Cap: ${snap['mcap']:,.0f} | Volume: ${snap['vol']:,.0f}\n"
        f"{'ML P(>=20% dip): ' + format(ml_note, '.0%') if ml_note is not None else ''}\n"
        f"{snap['ts']}\n"
    )
    return subject, html, text
