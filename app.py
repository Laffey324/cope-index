import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="COPE Index",
    page_icon="🛢️",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #F2F2F7;
    }
    [data-testid="stHeader"] {
        background-color: #F2F2F7 !important;
    }
    [data-testid="stToolbar"] {
        background-color: #F2F2F7 !important;
    }
    header[data-testid="stHeader"] {
        background-color: #F2F2F7 !important;
    }
    .stApp {
        background-color: #F2F2F7;
    }
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #1a1a1a !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdownContainer"] p {
        color: #1a1a1a !important;
    }
    hr {
        border-color: #c0c0c0 !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_current_wti():
    ticker = yf.Ticker("BZ=F")
    df = ticker.history(period="5d")[["Close"]]
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna()
    latest = float(df["Close"].iloc[-1])
    prev = float(df["Close"].iloc[-2])
    return latest, latest - prev

try:
    wti_price, wti_change = get_current_wti()
    wti_str = f"${wti_price:.2f}"
    wti_chg_str = f"+{wti_change:.2f}" if wti_change > 0 else f"{wti_change:.2f}"
    wti_color = "#4ade80" if wti_change > 0 else "#f87171"
except:
    wti_str = "N/A"
    wti_chg_str = ""
    wti_color = "#888"

total_score = round((10 + 10 + 7 + 5) / 4, 1)
risk_label = "CRITICAL" if total_score >= 8 else "ELEVATED" if total_score >= 6 else "MODERATE"
risk_color = "#f87171" if total_score >= 8 else "#fbbf24" if total_score >= 6 else "#4ade80"

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0a2342 0%, #1a3a5c 100%);
    padding: 36px 48px;
    border-radius: 12px;
    margin-bottom: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="flex:1;">
        <div style="font-size:13px; font-weight:700; color:#90c8f0; letter-spacing:3px; text-transform:uppercase; margin-bottom:10px;">
            CRUDE OIL POLICY & EVENT RISK DASHBOARD
        </div>
        <div style="font-size:56px; font-weight:900; color:#ffffff; letter-spacing:-2px; line-height:1; margin-bottom:6px;">
            COPE Index
        </div>
        <div style="font-size:13px; color:#b8d4e8; margin-top:14px; padding-top:14px; border-top:1px solid rgba(255,255,255,0.2);">
            Tracking how geopolitical events and policy signals translate into crude oil price risk
            &nbsp;·&nbsp;
            Last updated: {datetime.now().strftime('%B %d, %Y %H:%M')} ET
        </div>
    </div>
    <div style="display:flex; gap:32px; margin-left:48px;">
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#b8d4e8; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">Brent Crude</div>
            <div style="font-size:32px; font-weight:800; color:#ffffff;">{wti_str}</div>
            <div style="font-size:13px; color:{wti_color}; margin-top:4px;">{wti_chg_str} vs prev day</div>
        </div>
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#b8d4e8; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">COPE Risk Score</div>
            <div style="font-size:32px; font-weight:800; color:{risk_color};">{total_score:.1f}/10</div>
            <div style="font-size:13px; color:{risk_color}; margin-top:4px;">{risk_label}</div>
        </div>
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#b8d4e8; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">Hormuz Status</div>
            <div style="font-size:28px; font-weight:800; color:#f87171;">🔴 CLOSED</div>
            <div style="font-size:13px; color:#f87171; margin-top:4px;">Since Feb 28, 2026</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块一
# ══════════════════════════════════════════
st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">🌍 COPE Geopolitical Risk Index</div>
</div>
""", unsafe_allow_html=True)
st.markdown("Current assessment of key geopolitical risk factors affecting crude oil supply.")

risk_factors = {
    "Iran War & Hormuz Risk": {
        "score": 10, "trend": "↑",
        "note": "Hormuz still closed — IRGC turned back 3 ships Mar 27, called Trump's 'open' claim a lie. Dual-track toll system in Yuan institutionalized. ~500mb cumulative supply lost. Brent $115, up 60% since war began."
    },
    "Middle East Conflict Risk": {
        "score": 10, "trend": "↑",
        "note": "Houthis formally entered war Mar 28 — firing ballistic missiles at Israel, threatening Yanbu port and Bab al-Mandab Strait. Saudi's only Hormuz bypass now in missile range. Last buffer route at risk."
    },
    "Russia Supply Disruption": {
        "score": 7, "trend": "↑",
        "note": "Ukraine drone strike hit Ust-Luga terminal Mar 26 — threatens 400,000 bpd refinery output. Kirishi refinery also struck. Two simultaneous supply shocks now active."
    },
    "US Energy Policy Uncertainty": {
        "score": 5, "trend": "↑",
        "note": "All policy tools exhausted. SPR below legal floor. April 6 deadline extended unilaterally — Iran denied requesting extension. Trump's verbal interventions no longer moving markets durably."
    },
}

total_score = round(sum(v["score"] for v in risk_factors.values()) / len(risk_factors), 1)

cols = st.columns(len(risk_factors))
for i, (factor, data) in enumerate(risk_factors.items()):
    with cols[i]:
        score = data["score"]
        color = "#ef4444" if score >= 7 else "#f59e0b" if score >= 4 else "#22c55e"
        st.markdown(f"""
        <div style="border-left:4px solid {color}; border-radius:6px; padding:20px 18px;
            box-shadow:0 1px 4px rgba(0,0,0,0.15); height:200px; display:flex; flex-direction:column; gap:10px;">
            <div style="font-size:12px; font-weight:700; color:#666; text-transform:uppercase; letter-spacing:0.8px;">{factor}</div>
            <div style="font-size:52px; font-weight:800; color:{color}; line-height:1;">
                {score}<span style="font-size:18px; font-weight:400; color:#888;">/10</span>
                <span style="font-size:18px;">{data['trend']}</span>
            </div>
            <div style="font-size:13px; color:#555; line-height:1.5;">{data['note']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:20px; margin-bottom:8px;">
    <div style="font-size:13px; font-weight:700; color:#888; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:12px;">SCORING METHODOLOGY</div>
    <div style="display:flex; gap:12px;">
        <div style="flex:1; background:#f0fdf4; border-top:3px solid #22c55e; border-radius:6px; padding:14px 16px;">
            <div style="font-size:20px; font-weight:800; color:#22c55e; margin-bottom:8px;">🟢 1–3</div>
            <div style="font-size:14px; color:#555; line-height:1.6;">Minimal supply impact. Event contained to marginal producers, market has fully priced in the risk.</div>
        </div>
        <div style="flex:1; background:#fffbeb; border-top:3px solid #f59e0b; border-radius:6px; padding:14px 16px;">
            <div style="font-size:20px; font-weight:800; color:#f59e0b; margin-bottom:8px;">🟡 4–6</div>
            <div style="font-size:14px; color:#555; line-height:1.6;">Material supply impact with alternatives available. OPEC has capacity to offset, outcome manageable.</div>
        </div>
        <div style="flex:1; background:#fff1f1; border-top:3px solid #ef4444; border-radius:6px; padding:14px 16px;">
            <div style="font-size:20px; font-weight:800; color:#ef4444; margin-bottom:8px;">🔴 7–9</div>
            <div style="font-size:14px; color:#555; line-height:1.6;">Major supply threat, limited alternatives, OPEC adjustment capacity constrained, outcome highly uncertain.</div>
        </div>
        <div style="flex:1; background:#ffe4e4; border-top:3px solid #7f1d1d; border-radius:6px; padding:14px 16px;">
            <div style="font-size:20px; font-weight:800; color:#7f1d1d; margin-bottom:8px;">🚨 10</div>
            <div style="font-size:14px; color:#555; line-height:1.6;">Historic supply shock, no viable alternative. Hormuz closure = 10: threatens ~20% of global seaborne oil.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块二
# ══════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_price_data():
    wti_raw = yf.download("CL=F", start="2000-01-01", auto_adjust=True, progress=False)
    wti = wti_raw[["Close"]].copy().reset_index()
    wti.columns = ["date", "wti"]
    wti["date"] = pd.to_datetime(wti["date"]).dt.tz_localize(None)
    wti["wti"] = pd.to_numeric(wti["wti"], errors="coerce")
    wti = wti.dropna().reset_index(drop=True)

    brent_raw = yf.download("BZ=F", start="2000-01-01", auto_adjust=True, progress=False)
    brent = brent_raw[["Close"]].copy().reset_index()
    brent.columns = ["date", "brent"]
    brent["date"] = pd.to_datetime(brent["date"]).dt.tz_localize(None)
    brent["brent"] = pd.to_numeric(brent["brent"], errors="coerce")
    brent = brent.dropna().reset_index(drop=True)

    return wti, brent

st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">📈 Crude Oil Price — WTI & Brent</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; gap:0; margin-bottom:4px;">
    <span style="font-size:15px; color:#555; padding-right:16px; border-right:2px solid #1a6faf;">WTI — North American benchmark</span>
    <span style="font-size:15px; color:#555; padding:0 16px; border-right:2px solid #1a6faf;">Brent — Global benchmark</span>
    <span style="font-size:15px; color:#555; padding-left:16px;">Spread widens during Middle East supply shocks</span>
</div>
""", unsafe_allow_html=True)
st.caption("Source: Yahoo Finance — Daily closing price, updated each trading day")

try:
    wti_df, brent_df = load_price_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wti_df["date"], y=wti_df["wti"], mode="lines", name="WTI", line=dict(color="#2196F3", width=1.5)))
    fig.add_trace(go.Scatter(x=brent_df["date"], y=brent_df["brent"], mode="lines", name="Brent", line=dict(color="#f59e0b", width=1.5)))

    for event in [
        {"date": pd.Timestamp("2008-07-03"), "label": "2008 Peak $147"},
        {"date": pd.Timestamp("2020-04-20"), "label": "COVID Crash"},
        {"date": pd.Timestamp("2026-02-28"), "label": "US-Iran War"},
    ]:
        fig.add_vline(x=event["date"].timestamp()*1000, line_dash="dash",
            line_color="rgba(150,150,150,0.5)", line_width=1.5,
            annotation_text=event["label"], annotation_position="top",
            annotation_font_size=10, annotation_font_color="#555",
            annotation_bgcolor="rgba(255,255,255,0.85)",
            annotation_bordercolor="rgba(150,150,150,0.4)", annotation_borderwidth=1)

    fig.update_layout(height=480, yaxis_title="USD per Barrel", hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.15)", range=[-10, 160]),
        xaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0), margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    wti_latest = float(wti_df["wti"].iloc[-1])
    wti_prev = float(wti_df["wti"].iloc[-2])
    brent_latest = float(brent_df["brent"].iloc[-1])
    brent_prev = float(brent_df["brent"].iloc[-2])
    spread = brent_latest - wti_latest

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("WTI Latest", f"${wti_latest:.2f}", f"{wti_latest-wti_prev:+.2f} vs prev day")
    with col2:
        st.metric("Brent Latest", f"${brent_latest:.2f}", f"{brent_latest-brent_prev:+.2f} vs prev day")
    with col3:
        st.metric("Brent-WTI Spread", f"${spread:.2f}", "Elevated = global supply tighter than US")
    with col4:
        st.metric("1-Month High (Brent)", f"${float(brent_df['brent'].tail(30).max()):.2f}")

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)


st.markdown("""
<div style="background:rgba(148,163,184,0.08); border-radius:10px; padding:20px 24px; margin-bottom:8px;">
    <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">China Manufacturing PMI — Demand Signal</div>
    <div style="font-size:13px; color:#999;">Demand-side weakness currently overridden by Hormuz supply shock</div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1, 1])
with col3:
    st.metric(label="Mar 2026 PMI", value="50.4", delta="+1.4 vs Feb (Back to Expansion)")
    st.caption("PMI >50 = expansion. China is the world's largest crude importer.")
    st.markdown("""
    <div style="background:rgba(148,163,184,0.1); border-left:3px solid #94a3b8; border-radius:6px; padding:14px 16px; margin-top:12px;">
        <div style="font-size:14px; color:#555; line-height:1.7;">
            China PMI rebounded to <strong>50.4 in March</strong> — back above 50 for the first time in months, driven by post-holiday restocking and seasonal production recovery.
            <br><br>
            However, energy cost impact is <strong>lagged</strong> — March data largely reflects pre-war orders. The full effect of $100+ oil on Chinese manufacturing costs will appear in April data. Supply shock continues to override demand signals: Brent at $115+.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pmis = pd.DataFrame({"month": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"], "pmi": [49.7, 49.3, 49.4, 49.3, 49.0, 50.4]})
    fig_pmi = go.Figure()
    fig_pmi.add_trace(go.Scatter(x=pmis["month"], y=pmis["pmi"], mode="lines+markers",
        line=dict(color="#2196F3", width=2), marker=dict(size=8)))
    fig_pmi.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="50 = Neutral")
    fig_pmi.update_layout(height=220, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.15)", range=[48, 53]), margin=dict(t=10, b=10))
    st.plotly_chart(fig_pmi, use_container_width=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块五
# ══════════════════════════════════════════
@st.cache_data(ttl=60)
def fetch_war_headlines():
    queries = ["Hormuz+tanker+oil+shipping", "Iran+war+ceasefire+oil"]
    articles = []
    for query in queries:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            response = requests.get(url, timeout=5)
            root = ET.fromstring(response.content)
            for item in root.findall(".//item")[:4]:
                title = item.findtext("title", "")
                source = item.findtext("source", "")
                pub_date = item.findtext("pubDate", "")[:16]
                link = item.findtext("link", "")
                if title and "[Removed]" not in title:
                    articles.append({"title": title, "source": source, "date": pub_date, "url": link, "title_lower": title.lower()})
        except:
            continue
    seen = set()
    unique = []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    unique = [a for a in unique if all(ord(c) < 128 for c in a["title"])]
    return unique[:8]

def assess_signals(articles):
    hormuz_kw = ["hormuz", "tanker", "shipping", "strait", "vessel", "transit"]
    hormuz_evidence = [a for a in articles if any(k in a["title_lower"] for k in hormuz_kw)][:3]
    if not hormuz_evidence:
        hormuz_evidence = articles[:3]
    open_kw = ["fully open", "reopened", "reopen", "ceasefire", "hormuz open", "shipping resumes"]
    open_hits = [a for a in hormuz_evidence if any(k in a["title_lower"] for k in open_kw)]
    hormuz_status = "🟡 Partial Recovery Signals" if len(open_hits) >= 2 else "🔴 Effectively Closed"
    hormuz_color = "#f59e0b" if len(open_hits) >= 2 else "#ef4444"

    # ── 手动更新 — 每天根据新闻判断修改下面四行
    war_signal = "🔴 Dual Blockade Stalemate — Iran Offers Hormuz-for-Nuclear-Delay, US Skeptical, Congress Presses War Powers Deadline"
    war_color = "#ef4444"
    war_bg = "rgba(239,68,68,0.06)"
    war_border = "#ef4444"

    escalation_kw = ["escalat", "attack", "strike", "bomb", "missile", "expand", "retaliat"]
    deescalation_kw = ["ceasefire", "negotiat", "peace", "diplomac", "deal", "truce", "talk"]
    escalation_hits = [a for a in articles if any(k in a["title_lower"] for k in escalation_kw)]
    deescalation_hits = [a for a in articles if any(k in a["title_lower"] for k in deescalation_kw)]
    war_evidence = (escalation_hits + deescalation_hits)[:3] if (escalation_hits or deescalation_hits) else articles[:3]

    return hormuz_status, hormuz_color, hormuz_evidence, war_signal, war_color, war_bg, war_border, war_evidence

st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">🎯 War Outlook & Price Scenarios</div>
</div>
""", unsafe_allow_html=True)
st.markdown("Real-time war trajectory assessment based on latest headlines — and what each scenario means for oil prices.")

try:
    articles = fetch_war_headlines()
    hormuz_status, hormuz_color, hormuz_evidence, war_signal, war_color, war_bg, war_border, war_evidence = assess_signals(articles)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.06); border-radius:10px; padding:16px 20px; margin-bottom:12px;">
            <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">Hormuz Strait Status</div>
            <div style="font-size:13px; color:#999;">Auto-updated from latest shipping news</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='font-size:22px; font-weight:800; color:" + hormuz_color + "; margin:8px 0 12px 0;'>" + hormuz_status + "</div>", unsafe_allow_html=True)
        st.markdown("**Supporting headlines:**")
        if hormuz_evidence:
            for a in hormuz_evidence:
                st.markdown(f"• [{a['title']}]({a['url']})  \n  *{a['source']} — {a['date']}*")
        else:
            st.caption("No specific Hormuz headlines found in latest fetch.")
        st.markdown("""
        <div style="background:rgba(239,68,68,0.06); border-left:3px solid #ef4444; border-radius:6px; padding:14px 16px; margin-top:16px;">
            <div style="font-size:14px; color:#555; line-height:1.8;">
                <strong>What to watch:</strong><br>
                ✅ Confirmed loaded tanker transit → immediate price reversal signal<br>
                ✅ Insurance markets reopen for Hormuz routes → recovery confirmed<br>
                ❌ Further strikes on Gulf infrastructure → sustained $100+ prices
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:rgba(33,150,243,0.06); border-radius:10px; padding:16px 20px; margin-bottom:12px;">
            <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">War Trajectory Signal</div>
            <div style="font-size:13px; color:#999;">Manually updated daily by analyst — based on latest news judgment</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='font-size:22px; font-weight:800; color:" + war_color + "; margin:8px 0 12px 0;'>" + war_signal + "</div>", unsafe_allow_html=True)
        st.markdown("**Supporting headlines:**")
        if war_evidence:
            for a in war_evidence:
                st.markdown(f"• [{a['title']}]({a['url']})  \n  *{a['source']} — {a['date']}*")
        else:
            st.caption("No specific war trajectory headlines found in latest fetch.")
        st.markdown(
            "<div style='background:" + war_bg + "; border-left:3px solid " + war_border + "; border-radius:6px; padding:14px 16px; margin-top:16px;'>"
            "<div style='font-size:14px; color:#555; line-height:1.7;'>"
            "<strong>Signal methodology:</strong> War trajectory is assessed daily by the analyst based on latest news. Supporting headlines are auto-fetched to provide context."
            "</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(148,163,184,0.08); border-radius:10px; padding:16px 20px; margin-bottom:16px;">
        <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">What Could Happen to Oil Prices?</div>
        <div style="font-size:13px; color:#999;">Directional assessment — no price targets, direction and risk balance only. Based on IEA Oil Market Report (March 2026).</div>
    </div>
    """, unsafe_allow_html=True)

    for s in [
        {"title": "🟢 Scenario A: Deal reached before April 6 — Hormuz reopens within 30 days", "direction": "Bearish — But L-Shaped, Not V-Shaped",
         "driver": "Goldman base case: Brent falls to $71 by Q4 if flows restored within 30 days. BUT: structural damage means no V-shaped recovery. SPR must be refilled — governments become massive price-insensitive buyers in late 2026/2027. Qatar LNG offline for 5 years. Engineering cold-start: production facilities take weeks to restart, insurance months to normalize. L-shaped price plateau, not a crash.",
         "bg": "rgba(34,197,94,0.06)", "border": "#22c55e", "color": "#166534", "dir_color": "#22c55e"},
        {"title": "🟡 Scenario B: Partial resolution — 60 to 90 days, Hormuz partially reopens", "direction": "Neutral with High Volatility",
         "driver": "Goldman 60-day scenario: Brent Q4 $93. Capital Alpha: 45% probability this is the outcome (fall 2026 resolution). Bab al-Mandab status becomes critical — if Houthis block Yanbu port, Saudi's bypass route fails even after Hormuz deal. Market reprices toward growth shock rather than inflation shock. Bond market already beginning this transition.",
         "bg": "rgba(245,158,11,0.06)", "border": "#f59e0b", "color": "#92400e", "dir_color": "#f59e0b"},
        {"title": "🔴 Scenario C: Closure extends beyond 90 days or into 2027", "direction": "Bullish — $200 scenario modeled by US government",
         "driver": "Capital Alpha: 35% probability war extends into 2027. US government actively modeling $200/bbl scenario. Houthis blocking Bab al-Mandab eliminates Saudi bypass — both chokepoints simultaneously disrupted. Goldman: Brent exceeds 2008 $147 record if Hormuz stays at 5% flow for 10 weeks. Demand destruction accelerates. Recession becomes base case, not tail risk.",
         "bg": "rgba(239,68,68,0.06)", "border": "#ef4444", "color": "#991b1b", "dir_color": "#ef4444"},
    ]:
        st.markdown(
            "<div style='background:" + s["bg"] + "; border-left:4px solid " + s["border"] + "; border-radius:8px; padding:18px 22px; margin-bottom:12px;'>"
            "<div style='font-size:15px; font-weight:700; color:" + s["color"] + "; margin-bottom:6px;'>" + s["title"] + "</div>"
            "<div style='font-size:18px; font-weight:800; color:" + s["dir_color"] + "; margin-bottom:10px;'>→ " + s["direction"] + "</div>"
            "<div style='font-size:14px; color:#888; line-height:1.7;'>" + s["driver"] + "</div>"
            "</div>", unsafe_allow_html=True)

    st.caption("⚠️ Scenarios are directional assessments based on IEA frameworks and historical geopolitical risk premiums. Not investment advice.")

except Exception as e:
    st.error(f"Error loading war outlook: {e}")

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块六
# ══════════════════════════════════════════
@st.cache_data(ttl=1800)
def fetch_policy_news():
    queries = ["Trump+oil+energy+policy+2026", "Trump+SPR+petroleum+reserve+2026", "White+House+energy+oil+sanctions+2026"]
    articles = []
    for query in queries:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            response = requests.get(url, timeout=5)
            root = ET.fromstring(response.content)
            for item in root.findall(".//item")[:3]:
                title = item.findtext("title", "")
                source = item.findtext("source", "")
                pub_date = item.findtext("pubDate", "")[:16]
                link = item.findtext("link", "")
                if title and "[Removed]" not in title:
                    articles.append({"title": title, "source": source, "date": pub_date, "url": link, "title_lower": title.lower()})
        except:
            continue
    seen = set()
    unique = []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    must_have = ["oil", "energy", "petroleum", "gas price", "spr", "reserve", "opec", "crude"]
    war_kw = ["hormuz", "tanker", "strait", "iran war", "kharg", "ceasefire"]
    opinion_sources = ["center for american progress", "heritage foundation", "brookings", "cato institute", "think tank"]
    filtered = [
        a for a in unique
        if any(k in a["title_lower"] for k in must_have)
        and not any(k in a["title_lower"] for k in war_kw)
        and not any(k in a["source"].lower() for k in opinion_sources)
        and "2025" not in a["date"]
        and "2024" not in a["date"]
    ]
    return filtered[:5]

st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">🇺🇸 Trump & White House Policy Tracker</div>
</div>
""", unsafe_allow_html=True)
st.markdown("How White House policy decisions are affecting crude oil markets — analyst interpretation of each action.")

policy_actions = [
    {
        "date": "Apr 30, 2026",
        "action": "Trump: 'Blockade is incredible, Iran economy crashing' — Congress presses War Powers deadline, Senator Murkowski demands credible plan within one week",
        "interpretation": "Trump today said the naval blockade is 'working as planned' and Iran wants a deal 'badly,' losing $500M+ per day. He appeared to discount need to resume bombing: 'I don't know that we need it. We might need it.' But congressional pressure is now acute: War Powers 60-day clock may have expired yesterday (April 29) or expires tomorrow (May 1) depending on legal interpretation. Senator Murkowski announced she will introduce authorization measure if no credible White House plan emerges within one week. Hegseth argues ceasefire days don't count toward 60-day total. This legal pressure creates a new timeline forcing Trump to either get congressional authorization, reach a deal, or resume and then quickly end hostilities.",
        "impact": "🟡 Neutral",
        "source_title": "Trump blockade working, War Powers deadline — CNN / NPR",
        "source_url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"
    },
    {
        "date": "Apr 28, 2026",
        "action": "Iran submits new proposal: open Hormuz immediately, postpone nuclear talks until after war ends — US signals skepticism",
        "interpretation": "Iran's latest offer through Pakistan: full Hormuz reopening to all traffic in exchange for deferring nuclear discussions to post-war negotiations. Tehran billboard photographed April 28 reads 'The Strait of Hormuz Remains Closed' — signaling domestic political constraints on any deal. US officials express skepticism: unlikely to accept in current form. Core US position remains: nuclear commitment must be part of any deal, not deferred. Iran's red line: nuclear enrichment is non-negotiable sovereign right. Analyst Mortazavi: 'Tehran will not move if US doesn't lift blockade, Washington will not do so if Iran does not open the strait.' Classic standoff — both sides need the other to move first.",
        "impact": "🟡 Neutral",
        "source_title": "Iran's Hormuz-for-nuclear-delay proposal — Al Jazeera",
        "source_url": "https://www.aljazeera.com/news/2026/4/28/whats-in-irans-latest-proposal-and-how-has-the-us-responded"
    },
    {
        "date": "Apr 11-12, 2026",
        "action": "Vance meets Iran's Ghalibaf in Islamabad — highest-level US-Iran direct talks since 1979. Talks fail on nuclear question.",
        "interpretation": "Historic moment: first direct senior-level US-Iran engagement since the Islamic Revolution. But the outcome confirmed the unbridgeable gap: Vance demanded Iran commit to never seeking nuclear weapons. Iran refused. US then launched formal naval blockade of Iranian ports on April 13 — any vessel originating from or destined for Iranian ports subject to interdiction. US Navy entered Hormuz for first time since war began. Iran threatened to attack US ships. Both blockades remain in place simultaneously.",
        "impact": "🔺 Bullish",
        "source_title": "Vance-Ghalibaf Islamabad talks — Britannica / NPR",
        "source_url": "https://www.britannica.com/event/2026-Iran-war"
    },
    {
        "date": "Apr 22, 2026",
        "action": "IRGC seizes 3 ships in Hormuz — US extends ceasefire indefinitely pending Iranian 'unified proposal'",
        "interpretation": "IRGC seized two vessels and disabled a third on the same day Trump extended the ceasefire. Iran FM called US port blockade 'an act of war.' Iran losing $500M/day per Trump. Kharg Island storage approaching capacity — Iranian oil wells risk forced shut-in. Tehran billboard reading 'Hormuz Remains Closed' reflects domestic political reality: Iranian leadership cannot be seen to capitulate on Hormuz without tangible US concessions.",
        "impact": "🔺 Bullish",
        "source_title": "IRGC seizes ships, ceasefire extended — CNN / Al Jazeera",
        "source_url": "https://www.cnn.com/2026/04/22/world/live-news/iran-war-us-trump-blockade-ceasefire"
    },
    {
        "date": "Apr 9, 2026",
        "action": "Oil rebounds +6% to $100 within 24hrs of ceasefire — L-shaped plateau confirmed by market itself",
        "interpretation": "Oil fell 16% on ceasefire announcement, recovered to $100 in one session. Market discovered IRGC screening unchanged. Commodity Context: even full Hormuz reopening = $10-20 immediate drop, then Brent stabilizes $80-90 due to infrastructure damage, supply chain disruption, SPR refill demand. The $70 world is gone. House of Commons Library confirms: both US and Iran blockades remain in place. Iran FM: 'We intend to devise a new arrangement to ensure secure maritime traffic' — Iranian control of Hormuz is post-war baseline.",
        "impact": "🔺 Bullish",
        "source_title": "Oil rebounds, L-shaped plateau — CNBC / House of Commons Library",
        "source_url": "https://www.cnbc.com/2026/04/09/oil-prices-today-wti-brent-iran-accuse-us-of-ceasefire-breach.html"
    },
    {
        "date": "Apr 7, 2026",
        "action": "Goldman / IEA / Rystad: physical damage structural — Brent floor $80-90 even in full resolution scenario",
        "interpretation": "Goldman: largest oil supply disruption in history. IEA: shock exceeds 1973+1979+2022 combined. Rystad: $25B+ infrastructure reconstruction costs. Iranian officials: $270B in direct and indirect damages within Iran — reparations demand is non-negotiable part of any settlement. Ras Laffan LNG export capacity down 17% permanently. South Pars petrochemicals gone. Shipping normalization: 2+ months minimum. The structural damage outlasts any political agreement by months to years.",
        "impact": "🔺 Bullish",
        "source_title": "Goldman / IEA / Rystad supply assessment",
        "source_url": "https://www.cnbc.com/2026/04/02/oil-prices-today-wti-brent-trump-speech-iran-war-.html"
    },
]

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div style="background:rgba(33,150,243,0.06); border-radius:10px; padding:16px 20px; margin-bottom:16px;">
        <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">Policy Actions & Analyst Interpretation</div>
        <div style="font-size:13px; color:#999;">Manually updated daily — each action assessed for oil price impact</div>
    </div>
    """, unsafe_allow_html=True)

    for p in policy_actions:
        if "Bearish" in p["impact"]:
            impact_bg, impact_border, impact_color = "rgba(34,197,94,0.06)", "#22c55e", "#22c55e"
        elif "Bullish" in p["impact"]:
            impact_bg, impact_border, impact_color = "rgba(239,68,68,0.06)", "#ef4444", "#ef4444"
        else:
            impact_bg, impact_border, impact_color = "rgba(245,158,11,0.06)", "#f59e0b", "#f59e0b"

        st.markdown(
            "<div style='background:" + impact_bg + "; border-left:4px solid " + impact_border + "; border-radius:8px; padding:16px 20px; margin-bottom:12px;'>"
            "<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>"
            "<div style='font-size:13px; color:#888;'>" + p["date"] + "</div>"
            "<div style='font-size:15px; font-weight:700; color:" + impact_color + ";'>" + p["impact"] + "</div>"
            "</div>"
            "<div style='font-size:15px; font-weight:700; color:#333; margin-bottom:10px;'>" + p["action"] + "</div>"
            "<div style='font-size:14px; color:#555; line-height:1.7; margin-bottom:10px;'>" + p["interpretation"] + "</div>"
            "<div style='font-size:13px;'>📰 <a href='" + p["source_url"] + "' style='color:#4a9fd4;'>" + p["source_title"] + "</a></div>"
            "</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:rgba(33,150,243,0.06); border-radius:10px; padding:16px 20px; margin-bottom:16px;">
        <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">Latest Policy Headlines</div>
        <div style="font-size:13px; color:#999;">Auto-fetched — Trump & White House energy policy only</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        policy_news = fetch_policy_news()
        if policy_news:
            for a in policy_news:
                st.markdown(f"• [{a['title']}]({a['url']})  \n  *{a['source']} — {a['date']}*")
        else:
            st.caption("No policy headlines found in latest fetch.")
    except Exception as e:
        st.error(f"Error fetching policy news: {e}")

    st.markdown("""
    <div style="background:rgba(239,68,68,0.06); border-left:3px solid #ef4444; border-radius:6px; padding:16px 18px; margin-top:20px;">
        <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:8px;">Current White House Stance</div>
        <div style="font-size:14px; color:#555; line-height:1.7;">
            Trump's signals are now the single largest source of oil price volatility.
            The 48-hour ultimatum moved markets up. The false ceasefire claim moved markets down 7%.
            Neither was grounded in verified reality — Iran denied both the threat's execution and the talks.
            <br><br>
            All conventional policy tools are exhausted. SPR below legal floor. Iranian sanctions lifted.
            Russian waivers issued. None moved prices durably.
            The 5-day postponement window expires Saturday — watch for whether Trump executes, extends, or backs down again.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块七：Analyst Notes
# ══════════════════════════════════════════
st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">📝 Analyst Notes</div>
</div>
""", unsafe_allow_html=True)
st.markdown(f"*Last updated: {datetime.now().strftime('%B %d, %Y')}*")

st.markdown("""
<div style="background:rgba(33,150,243,0.06); border-radius:10px; padding:24px 28px; margin-bottom:16px;">
    <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">MARKET THESIS</div>
    <div style="font-size:13px; color:#999; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Core Thesis</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
        Brent is trading above $110/bbl — up over 45% since the war began on February 28.
        Every policy tool Washington has deployed — SPR release, Russia sanctions easing, Iranian crude unsanctioning —
        has failed to move prices. The market is pricing one thing only: Hormuz is closed, and neither side wants to end the war.
        Iraq's force majeure, Qatar's permanent LNG loss, and the cascade of Gulf infrastructure damage
        mean the supply disruption is now self-compounding.
        DXY, China PMI, and IEA reserves are all secondary until tanker traffic resumes.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background:rgba(239,68,68,0.08); border-left:3px solid #ef4444; border-radius:6px; padding:16px 18px;">
        <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:12px;">🔺 Key Upside Risks</div>
        <div style="font-size:14px; color:#444; line-height:2.0;">
            • Hormuz closure compounds — Goldman estimates 97% flow reduction, escorts restore at most 20%<br>
            • Recession is the second shoe — market has only priced inflation, not growth destruction<br>
            • Trump power plant ultimatum escalates — Iran retaliates against desalination across Gulf<br>
            • Marines seize Kharg Island — permanent loss of 85–95% of Iran's export capacity<br>
            • Nuclear escalation — Iran struck Dimona vicinity; Israeli retaliation could internationalise conflict
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:rgba(34,197,94,0.08); border-left:3px solid #22c55e; border-radius:6px; padding:16px 18px;">
        <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:12px;">🔻 Key Downside Risks</div>
        <div style="font-size:14px; color:#444; line-height:2.0;">
            • Ceasefire or Hormuz reopening — Goldman base case: Brent falls to $71 by Q4 if restored within 30 days<br>
            • Demand destruction accelerating — $113 Brent already triggering recession risk in Europe and Asia<br>
            • Goldman 60-day scenario: Brent $93 Q4 — market reprices toward growth shock, not inflation<br>
            • US shale response — rig count rising, non-OPEC supply increasing<br>
            • China demand weakness — PMI below 50 for 6 months, imports softening<br>
            • Fed forced rate hikes — Goldman pushes first cut to September; hikes possible if inflation persists
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(26,111,175,0.1); border-left:4px solid #1a6faf; border-radius:6px; padding:18px 20px; margin-top:16px;">
    <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:10px;">Analyst View — April 30, 2026</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
        Two months into this war, the situation has settled into
        a structured stalemate that neither side can easily exit.
        The US blockades Iranian ports.
        Iran controls Hormuz and refuses unconditional opening.
        Both sides are inflicting economic pain.
        Both sides claim leverage.
        Neither side has the political room to make the first concession.
        <br><br>
        Iran's latest proposal — open Hormuz now,
        defer nuclear talks until after the war ends —
        is actually the most pragmatic offer Tehran has made.
        It separates the immediate economic crisis
        from the existential strategic question.
        The problem is that for Washington and Israel,
        the nuclear question IS the war.
        Trump went to war to prevent Iran from getting a bomb.
        Accepting a Hormuz deal that postpones nuclear discussions
        indefinitely gives Iran time to reconstitute
        exactly what the war was meant to destroy.
        The US skepticism is structurally rational,
        even if the human cost of continued stalemate is severe.
        <br><br>
        The War Powers clock adds a new dimension this week.
        Whether the 60-day deadline was yesterday or tomorrow
        depends on legal interpretation —
        but the political pressure is real and immediate.
        Senator Murkowski's one-week ultimatum to the White House
        forces Trump to show his hand:
        is the blockade a pressure tactic toward a deal,
        or is it open-ended economic warfare with no exit?
        If Congress moves toward authorization or termination,
        the diplomatic timeline compresses sharply.
        <br><br>
        For oil markets, the structural picture is unchanged.
        Brent is still 35-40% above pre-war levels
        after a ceasefire, a naval blockade, three rounds of talks,
        and two months of diplomacy.
        The House of Commons Library confirmed this week:
        neither blockade has been removed.
        Iran's FM has said explicitly that post-war Hormuz
        will operate under 'a new arrangement' —
        meaning Iranian management.
        The $70 world required a free Hormuz.
        That Hormuz no longer exists.
        The floor is $80-90 in the most optimistic scenario,
        and we are not yet in that scenario.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.subheader("⚖️ War Will Analysis — Evidence-Based Scoring")
st.caption("Each score is derived from cited evidence, not editorial opinion. Click any dimension to see the reasoning.")

# ── DATA ─────────────────────────────────────────────────────────────────────

us_dimensions = [
    {
        "name": "Military capacity",
        "score": 8,
        "prev_score": 8,
        "evidence": [
            {"text": "US Navy forced 28 ships to turn back under Hormuz blockade without operational degradation", "source": "NPR", "url": "https://www.npr.org/2026/04/21/nx-s1-5793638/iran-middle-east-updates"},
            {"text": "B-2 and carrier strike groups remain on station in the Gulf", "source": "CNN", "url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"},
            {"text": "Kharg Island, South Pars, bridges and rail struck with precision — no operational degradation reported", "source": "NPR", "url": "https://www.npr.org/2026/04/07/nx-s1-5776377/iran-war-updates"},
        ],
        "verdict": "Military capability remains the US's strongest card. No signs of ammunition shortage or operational fatigue reported publicly."
    },
    {
        "name": "White House internal consensus",
        "score": 4,
        "prev_score": 5,
        "evidence": [
            {"text": "Chief of Staff Wiles told colleagues situation 'may be losing control'", "source": "Time / Wall Street CN", "url": "https://wallstreetcn.com/articles/3769247"},
            {"text": "Vance was strongest war opponent, excluded from opening night decision circle", "source": "Time / Wall Street CN", "url": "https://wallstreetcn.com/articles/3769247"},
            {"text": "Hegseth 'blindsided' by Iran's scale of retaliation", "source": "Time / Wall Street CN", "url": "https://wallstreetcn.com/articles/3769247"},
            {"text": "Trump aides believe Iranian leadership is fractured — used as justification to extend ceasefire rather than re-escalate", "source": "CNN", "url": "https://www.cnn.com/2026/04/22/world/live-news/iran-war-us-trump-blockade-ceasefire"},
        ],
        "verdict": "Real internal disagreement. Vance faction pushing diplomatic exit; Hegseth faction favoring pressure. Trump navigating between them rather than committing to either."
    },
    {
        "name": "Domestic political pressure",
        "score": 4,
        "prev_score": 6,
        "evidence": [
            {"text": "National average gasoline above $4/gallon — historically a major drag on presidential approval", "source": "NPR", "url": "https://www.npr.org/2026/04/21/nx-s1-5793638/iran-middle-east-updates"},
            {"text": "Senator Murkowski: War Powers authorization measure if no credible White House plan within one week", "source": "CNN", "url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"},
            {"text": "War Powers 60-day deadline expired Apr 29 or May 1 — legal pressure now acute", "source": "CNN", "url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"},
            {"text": "Chicago Fed's Goolsbee: oil shock threatens 2026 rate cuts", "source": "Wall Street CN", "url": "https://wallstreetcn.com/articles/3769247"},
        ],
        "verdict": "$4 gasoline + War Powers deadline + congressional pushback form a convergent pressure point in May. This is the most acute constraint on Trump's war options."
    },
    {
        "name": "Midterm election calculus",
        "score": 5,
        "prev_score": 5,
        "evidence": [
            {"text": "Historical precedent: presidents with unresolved wars at midterms lose seats — 2006 Iraq analogy cited by analysts", "source": "Britannica", "url": "https://www.britannica.com/event/2026-Iran-war"},
            {"text": "Trump approval closely tied to gas price trajectory — $4+ is the historical inflection point", "source": "NPR", "url": "https://www.npr.org/2026/04/21/nx-s1-5793638/iran-middle-east-updates"},
            {"text": "A decisive military 'win' (Hormuz reopened, nuclear deal) would be electorally positive — but that outcome is not in sight", "source": "CNN", "url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"},
        ],
        "verdict": "Balanced risk. A prolonged stalemate into fall 2026 is negative for midterms. A clean resolution before Q3 could be positive. Current trajectory leans negative."
    },
    {
        "name": "Fiscal cost tolerance",
        "score": 6,
        "prev_score": 6,
        "evidence": [
            {"text": "US carrying ~$36T in national debt with $10T rolling over next year — fiscal headroom is limited", "source": "Wall Street CN", "url": "https://wallstreetcn.com/articles/3769199"},
            {"text": "No official war cost estimate released publicly — CBO has not scored the operation", "source": "CNN", "url": "https://www.cnn.com/2026/04/30/world/live-news/iran-war-news"},
            {"text": "Naval blockade is lower-cost than active bombing campaign — current posture is fiscally more sustainable", "source": "NPR", "url": "https://www.npr.org/2026/04/22/nx-s1-5795405/iran-middle-east-updates"},
            {"text": "SPR released 172mb — now at ~244mb, below 252mb legal minimum. Remaining headroom ~80-90mb maximum before emergency declaration required", "source": "IEA / Goldman Sachs", "url": "https://www.goldmansachs.com"},
        ],
        "verdict": "Moderate pressure. The shift to naval blockade from kinetic strikes reduces daily cost. Fiscal constraint is real but not yet the binding constraint."
    },
    {
        "name": "Allied support",
        "score": 5,
        "prev_score": 5,
        "evidence": [
            {"text": "30+ countries meeting at RAF base to plan multinational Hormuz security mission — but only after 'sustained ceasefire'", "source": "NPR", "url": "https://www.npr.org/2026/04/22/nx-s1-5795405/iran-middle-east-updates"},
            {"text": "UN Security Council Hormuz resolution vetoed by China, Russia, France — multilateral legal path closed", "source": "CNBC", "url": "https://www.cnbc.com/2026/04/03/trump-iran-threats-un-resolution-blocked-strait-of-hormuz-f35-shot-down.html"},
            {"text": "Trump criticized NATO on Truth Social: 'NATO wasn't there when we needed them'", "source": "TheStreet", "url": "https://www.thestreet.com/latest-news/stock-market-today-apr-9-2026-updates"},
            {"text": "Spain PM: 'will not applaud those who set the world on fire just because they show up with a bucket'", "source": "Wikipedia / multiple", "url": "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire"},
        ],
        "verdict": "Allies are sympathetic to Hormuz reopening but not to the war itself. The US is operating largely unilaterally. Allied support is conditional and post-conflict, not wartime."
    },
]

iran_dimensions = [
    {
        "name": "Economic bearing capacity",
        "score": 3,
        "prev_score": 5,
        "evidence": [
            {"text": "Trump: Iran losing '$500 million per day' — military and police not being paid", "source": "NPR", "url": "https://www.npr.org/2026/04/22/nx-s1-5795405/iran-middle-east-updates"},
            {"text": "Kharg Island storage approaching capacity — oil wells at risk of forced shut-in within days", "source": "NPR", "url": "https://www.npr.org/2026/04/22/nx-s1-5795405/iran-middle-east-updates"},
            {"text": "South Pars petrochemicals destroyed — 85% of petrochemical export revenue gone", "source": "NPR", "url": "https://www.npr.org/2026/04/07/nx-s1-5776377/iran-war-updates"},
            {"text": "Iranian president: reparations are 'the only way' to end conflict", "source": "House of Commons Library", "url": "https://commonslibrary.parliament.uk/research-briefings/cbp-10637/"},
        ],
        "verdict": "Iran's economy is under severe and accelerating stress. The US blockade is the primary lever. This is Iran's weakest dimension and the binding constraint on how long it can hold out."
    },
    {
        "name": "Military retaliation capacity",
        "score": 6,
        "prev_score": 7,
        "evidence": [
            {"text": "US intelligence: Iran retains ~50% of missile launchers intact despite weeks of strikes", "source": "Time / Wall Street CN", "url": "https://wallstreetcn.com/articles/3769247"},
            {"text": "IRGC seized two vessels and disabled a third in Hormuz on Apr 22 — real-time enforcement capability intact", "source": "CNN", "url": "https://www.cnn.com/2026/04/22/world/live-news/iran-war-us-trump-blockade-ceasefire"},
            {"text": "IRGC threatened to target oil facilities in neighboring countries if US resumes strikes from their territory", "source": "NPR", "url": "https://www.npr.org/2026/04/21/nx-s1-5793638/iran-middle-east-updates"},
        ],
        "verdict": "Degraded but not destroyed. Iran can still inflict meaningful pain on Gulf states and shipping. The 50% launcher retention is the key number — enough for continued deterrence."
    },
    {
        "name": "Hormuz leverage",
        "score": 9,
        "prev_score": 9,
        "evidence": [
            {"text": "Trump proposed US-Iran 'joint venture' to co-manage Hormuz — first US acknowledgment of Iranian sovereign role", "source": "Wall Street CN", "url": "https://wallstreetcn.com/articles/3769503"},
            {"text": "Iran's FM: 'We intend to devise a new arrangement to ensure secure maritime traffic' — post-war Iranian control is baseline", "source": "House of Commons Library", "url": "https://commonslibrary.parliament.uk/research-briefings/cbp-10637/"},
            {"text": "Citrini field report: IRGC enforcement fully operational, ~50% of Hormuz traffic invisible to AIS", "source": "Wall Street CN", "url": "https://wallstreetcn.com/articles/3769308"},
        ],
        "verdict": "Hormuz remains Iran's most powerful and durable card. Even Trump has accepted Iranian co-management as the post-war baseline. This leverage does not diminish regardless of military setbacks."
    },
    {
        "name": "Leadership internal consensus",
        "score": 5,
        "prev_score": 7,
        "evidence": [
            {"text": "Trump aides: Iran does not have consensus — negotiators cannot be empowered to finalize a deal", "source": "CNN", "url": "https://www.cnn.com/2026/04/22/world/live-news/iran-war-us-trump-blockade-ceasefire"},
            {"text": "Parliament speaker Ghalibaf said ceasefire and negotiations are 'unreasonable' — contradicting FM Araghchi", "source": "Wikipedia / multiple", "url": "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire"},
            {"text": "Tehran billboard Apr 28: 'The Strait of Hormuz remains closed' — domestic signaling constrains negotiators", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2026/4/28/whats-in-irans-latest-proposal-and-how-has-the-us-responded"},
        ],
        "verdict": "Iran's leadership is fractured between IRGC hardliners and the diplomatic track. This internal split is the primary reason talks keep stalling — negotiators cannot make binding commitments."
    },
    {
        "name": "International diplomatic support",
        "score": 6,
        "prev_score": 6,
        "evidence": [
            {"text": "China and Russia vetoed UN Security Council Hormuz resolution — protecting Iran's position at the multilateral level", "source": "CNBC", "url": "https://www.cnbc.com/2026/04/03/trump-iran-threats-un-resolution-blocked-strait-of-hormuz-f35-shot-down.html"},
            {"text": "Iran's ambassador to China: international guarantees could include China, Pakistan, Turkey, Russia", "source": "House of Commons Library", "url": "https://commonslibrary.parliament.uk/research-briefings/cbp-10637/"},
            {"text": "Lloyd's List tracked 'shadow fleet' vessels moving in and out of Iranian ports despite blockade", "source": "NPR", "url": "https://www.npr.org/2026/04/21/nx-s1-5793638/iran-middle-east-updates"},
        ],
        "verdict": "China and Russia provide meaningful diplomatic cover and shadow fleet support. Not enough to break the economic siege but enough to prevent total isolation."
    },
    {
        "name": "Public will to resist",
        "score": 7,
        "prev_score": 7,
        "evidence": [
            {"text": "Tehran crowds celebrated ceasefire announcement — nationalist sentiment remains strong", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2026/4/8/us-iran-ceasefire-deal-what-are-the-terms-and-whats-next"},
            {"text": "Tehran billboard 'Hormuz remains closed' reflects domestic political constraint — leadership cannot be seen to capitulate", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2026/4/28/whats-in-irans-latest-proposal-and-how-has-the-us-responded"},
            {"text": "Historical precedent: Iran sustained 8 years of Iraq war under severe economic pressure 1980-1988", "source": "Britannica", "url": "https://www.britannica.com/event/2026-Iran-war"},
        ],
        "verdict": "Iranian public nationalism is a genuine constraint on any deal that looks like surrender. Historical precedent suggests Iranians can absorb severe economic pain if the framing is resistance rather than defeat."
    },
]

# ── RENDER FUNCTION ────────────────────────────────────────────────────────────

def render_war_will(dimensions, color):
    for dim in dimensions:
        score = dim["score"]
        prev = dim["prev_score"]
        delta = score - prev
        if delta > 0:
            trend = f"↑ +{delta} from last update"
        elif delta < 0:
            trend = f"↓ {delta} from last update"
        else:
            trend = "→ unchanged"

        bar_pct = int(score * 10)
        label = f"{dim['name']}  —  {score}/10  ({trend})"

        with st.expander(label):
            st.progress(bar_pct)
            for ev in dim["evidence"]:
                st.markdown(f"- {ev['text']} &nbsp; [[{ev['source']}]]({ev['url']})")
            st.info(f"**Assessment:** {dim['verdict']}")

# ── LAYOUT ─────────────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    us_avg = sum(d["score"] for d in us_dimensions) / len(us_dimensions)
    st.markdown(f"### 🇺🇸 United States")
    st.caption(f"Average score: **{us_avg:.1f} / 10** &nbsp;·&nbsp; {len(us_dimensions)} dimensions &nbsp;·&nbsp; Apr 30, 2026")
    render_war_will(us_dimensions, "#378ADD")

with col2:
    ir_avg = sum(d["score"] for d in iran_dimensions) / len(iran_dimensions)
    st.markdown(f"### 🇮🇷 Iran")
    st.caption(f"Average score: **{ir_avg:.1f} / 10** &nbsp;·&nbsp; {len(iran_dimensions)} dimensions &nbsp;·&nbsp; Apr 30, 2026")
    render_war_will(iran_dimensions, "#E24B4A")