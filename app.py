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
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1a1a1a !important;
    }
    .stMarkdown p, .stMarkdown li {
        color: #1a1a1a !important;
    }
    [data-testid="stSubheader"] {
        color: #1a1a1a !important;
    }
    [data-testid="stSubheader"] p {
        color: #1a1a1a !important;
    }
    .stApp [data-testid="stHeading"] {
        color: #1a1a1a !important;
    }
    .stApp [data-testid="stHeading"] * {
        color: #1a1a1a !important;
    }
    [data-testid="stExpander"] summary p {
        color: #1a1a1a !important;
    }
    [data-testid="stCaptionContainer"] p {
        color: #666666 !important;
    }
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
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

total_score = round((8 + 7 + 6 + 6) / 4, 1)
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
            <div style="font-size:28px; font-weight:800; color:#f59e0b;">● UNSTABLE</div>
            <div style="font-size:13px; color:#f59e0b; margin-top:4px;">~35 ships/day but fighting resumed July 14</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块一
# ══════════════════════════════════════════
st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700; color:#1a1a1a;">🌍 COPE Geopolitical Risk Index</div>
</div>
""", unsafe_allow_html=True)
st.markdown("Current assessment of key geopolitical risk factors affecting crude oil supply.")

risk_factors = {
    "Iran War & Hormuz Risk": {
        "score": 8, "trend": "↑",
        "note": "MOU collapsing — US-Iran fighting resumed July 14 for third consecutive day. Brent surged to $85.92, highest since June 15. Nuclear inspection dispute: US insists IAEA access to bombed sites, Iran denies agreeing. MOU 60-day window expires mid-August."
    },
    "Middle East Conflict Risk": {
        "score": 7, "trend": "↑",
        "note": "Lebanon violence resumed June 23. Israel-Hezbollah exchanges ongoing. Iran FM warned of 'immediate powerful response' to any Israeli attack. MOU did not resolve Lebanon question — Israel never formally joined ceasefire."
    },
    "Russia Supply Disruption": {
        "score": 6, "trend": "→",
        "note": "Ukraine drone strikes on Russian energy infrastructure ongoing. Russia shadow fleet continuing to operate. Market attention returning to Russia risk as Iran MOU shows signs of collapse."
    },
    "US Energy Policy Uncertainty": {
        "score": 6, "trend": "↑",
        "note": "60-day MOU window expiring mid-August. Nuclear inspection dispute threatens to unwind entire framework. SPR refill demand ongoing. Goldman: Brent could exceed $130 if exports only gradually recover."
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
    <div style="font-size:22px; font-weight:700; color:#1a1a1a;">📈 Crude Oil Price — WTI & Brent</div>
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
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(color="#1a1a1a")), margin=dict(t=40, b=20))
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
    st.metric(label="May 2026 PMI", value="50.0", delta="-0.3 vs Apr (Demand Softening)")
    st.caption("PMI >50 = expansion. China is the world's largest crude importer.")
    st.markdown("""
    <div style="background:rgba(148,163,184,0.1); border-left:3px solid #94a3b8; border-radius:6px; padding:14px 16px; margin-top:12px;">
        <div style="font-size:14px; color:#555; line-height:1.7;">
            China PMI slipped to <strong>50.0 in May</strong>, down from 50.3 in April and 50.4 in March. Still technically in expansion but barely — new orders index fell to 49.9, back in contraction territory.
            <br><br>
            The oil shock is showing up in the data. <strong>Demand is softening</strong> while production output (51.2) holds up — a classic stagflation pattern: supply-side costs elevated, demand-side weakening. Foreign orders also declined. With Brent still ~$91 and the MOU not yet signed, the June and July PMI readings will be the key signal for whether demand destruction is accelerating.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pmis = pd.DataFrame({"month": ["Dec", "Jan", "Feb", "Mar", "Apr", "May"], "pmi": [49.4, 49.3, 49.0, 50.4, 50.3, 50.0]})
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
    hormuz_status = "� CLOSED Recovery Signals" if len(open_hits) >= 2 else "🔴 Effectively Closed"
    hormuz_color = "#f59e0b" if len(open_hits) >= 2 else "#ef4444"

    # ── 手动更新 — 每天根据新闻判断修改下面四行
    war_signal = "🔴 MOU Collapsing — US-Iran Fighting Resumed July 14, Nuclear Inspection Dispute, Brent Surges to $86"
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
    <div style="font-size:22px; font-weight:700; color:#1a1a1a;">🎯 War Outlook & Price Scenarios</div>
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
        {"title": "🟢 Scenario A: MOU signed, Hormuz fully reopens by July", "direction": "Bearish — L-Shaped, Floor at $80",
         "driver": "Wood Mackenzie: Brent eases to ~$80 by end of 2026 if deal by June. Aramco CEO: even if Hormuz opens today, takes months to rebalance. SPR refill demand creates structural floor. Kharg Island damage, South Pars gone, shipping insurance not normalizing for months. The $70 world is gone — $80 is the best case.",
         "bg": "rgba(34,197,94,0.06)", "border": "#22c55e", "color": "#166534", "dir_color": "#22c55e"},
        {"title": "🟡 Scenario B: MOU stalls, partial Hormuz flow continues into Q3", "direction": "Neutral — Brent $90-100 Range",
         "driver": "Current base case. ~24 ships/day through Hormuz vs 100+ pre-war. Both sides trading strikes while negotiating. Aramco CEO: delay past mid-June and normalization goes to 2027. Market pricing partial resolution but not full reopening. High volatility on any Trump/Iran headline.",
         "bg": "rgba(245,158,11,0.06)", "border": "#f59e0b", "color": "#92400e", "dir_color": "#f59e0b"},
        {"title": "🔴 Scenario C: MOU collapses, full re-escalation resumes", "direction": "Bullish — Return to $110-115+",
         "driver": "Khamenei declared US bases 'no longer safe' June 2. IRGC still firing on vessels. If Trump refuses to sign MOU and resumes bombing campaign, Hormuz returns to near-full closure. Aramco: normalization to 2027. Hochstein warns of energy market 'cliff' if no deal by June.",
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
    <div style="font-size:22px; font-weight:700; color:#1a1a1a;">🇺🇸 Trump & White House Policy Tracker</div>
</div>
""", unsafe_allow_html=True)
st.markdown("How White House policy decisions are affecting crude oil markets — analyst interpretation of each action.")

policy_actions = [
    {
        "date": "Jul 14-26, 2026",
        "action": "US-Iran fighting resumed for third consecutive day — Brent surges to $85.92, highest since June 15. MOU framework collapsing over nuclear inspection dispute.",
        "interpretation": "The 60-day MOU signed June 19 in Geneva is showing severe signs of collapse. US-Iran military exchanges resumed in mid-July — the third time fighting has restarted since the original February 28 war began. Brent surged 3.8% on July 14, extending a 9.6% gain from the previous day, reaching $85.92 — erasing most of the post-MOU price decline. Core dispute: US insists IAEA inspectors must access Iran's bombed nuclear sites. Iran denies ever agreeing to this. Vance had declared IAEA access 'a major milestone' on June 21 — Iran says this was never part of the deal. Goldman scenario now in play: if exports only gradually recover and Hormuz never fully reopens, Brent could exceed $130 by year-end. The MOU 60-day clock expires mid-August. If no permanent deal is reached, the entire framework collapses.",
        "impact": "🔺 Bullish",
        "source_title": "MOU collapsing, Brent $86, fighting resumed — Al Jazeera / Goldman Sachs",
        "source_url": "https://www.aljazeera.com/economy/2026/7/14/oil-hits-1-month-high-as-us-iran-fighting-clouds-strait-of-hormuz-outlook"
    },
    {
        "date": "Jul 7, 2026",
        "action": "Iran attacks Qatari tanker near Hormuz — Brent +3% to $74.16. First major post-MOU maritime incident.",
        "interpretation": "Iran attacked a tanker from Qatar near Hormuz just three weeks after the MOU was signed. Brent rose 3% to $74.16. The attack confirmed what the dashboard argued since June 15: Hochstein was right — Iranians control Hormuz regardless of what any document says. The MOU did not change the physical enforcement reality. IRGC retained capability and willingness to strike vessels even during the nominal ceasefire period.",
        "impact": "🔺 Bullish",
        "source_title": "Iran attacks Qatari tanker, Brent +3% — CNBC",
        "source_url": "https://www.cnbc.com/2026/07/07/oil-prices-iran-strait-hormuz.html"
    },
    {
        "date": "Jun 21-23, 2026",
        "action": "US-Iran reach 'road map' framework. Vance: IAEA access 'major milestone.' Iran disputes nuclear inspection terms two days later.",
        "interpretation": "June 21: Vance announced 'a lot of good progress' — Iran agreed to invite IAEA inspectors back, technical talks began immediately. June 23: Iran disputed whether it had agreed to IAEA access to bombed nuclear sites. Same day, Lebanon violence resumed. The pattern: every apparent breakthrough in this conflict has been followed within days by a contradiction from the other side. The nuclear inspection question — what exactly Iran agreed to — is now the central fault line.",
        "impact": "🟡 Neutral",
        "source_title": "Road map framework, IAEA dispute — NPR",
        "source_url": "https://www.npr.org/2026/06/21/g-s1-129222/us-iran-deal-lebanon-israel-strait-hormuz-jd-vance"
    },
    {
        "date": "Jun 19, 2026",
        "action": "MOU signed in Geneva — war formally ends. Hormuz begins reopening. WTI -5.5% to $80, Brent -5% to $83.",
        "interpretation": "The 116-day war formally ended June 19. Hormuz began reopening — 300 tankers cleared the backlog, traffic rose to ~35 ships/day by July 1. Oil fell sharply on the announcement. But the L-shaped plateau thesis was immediately validated: Brent Feb 2027 futures settled at $80. And within three weeks, fighting had resumed and Brent was back at $86. The MOU was a political framework, not a physical resolution.",
        "impact": "🔻 Bearish",
        "source_title": "MOU signed, war ends — Axios",
        "source_url": "https://www.axios.com/2026/06/14/us-iran-ceasefire-extended-hormuz-reopen-trump"
    },
    {
        "date": "Apr 9, 2026",
        "action": "L-shaped plateau confirmed: oil -16% on ceasefire, +6% next session. Now re-confirmed: Brent back to $86 just five weeks after MOU.",
        "interpretation": "The April 9 thesis has now been validated twice. First on June 15 when MOU was announced and Brent Feb 2027 futures held at $80. Now in July when fighting resumed and Brent snapped back to $86 within five weeks of the MOU. The market cannot price a clean resolution because no clean resolution exists. Goldman: if Hormuz never fully reopens, Brent could exceed $130. If it reopens quickly, Brent at $60 in 2027. The enormous range reflects genuine uncertainty. Goldman: 'You can't jawbone molecules.'",
        "impact": "🔺 Bullish",
        "source_title": "L-shaped plateau — re-confirmed",
        "source_url": "https://www.cnbc.com/2026/04/09/oil-prices-today-wti-brent-iran-accuse-us-of-ceasefire-breach.html"
    },
    {
        "date": "Feb 28 — Jul 26, 2026",
        "action": "148-day war summary: Brent $70 → $115 peak → $83 MOU → $74 low → $86 today. MOU collapsing. Nuclear deal unresolved.",
        "interpretation": "The war is now 148 days old. The MOU signed June 19 has not produced a permanent deal. Fighting has resumed multiple times. The nuclear inspection question — the core issue that started the war — remains unresolved. Goldman's two scenarios: $130+ if Hormuz stays restricted, $60 if it reopens fully. Today's $86 Brent reflects the market's uncertainty between these two outcomes. Neither side has won. Neither side has lost. The war continues in a different form.",
        "impact": "🟡 Neutral",
        "source_title": "148-day war — ongoing",
        "source_url": "https://commonslibrary.parliament.uk/research-briefings/cbp-10637/"
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
            Today Trump cancelled strikes planned for tonight and claimed the deal is 'almost done' — his 38th such announcement per CreditSights. Iran denied approving any text. Watch for Iran's official confirmation to the Pakistani mediator — that is the only signal that counts.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, rgba(26,111,175,0.1)); margin:32px 0; opacity:1;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块七：Analyst Notes
# ══════════════════════════════════════════
st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700; color:#1a1a1a;">📝 Analyst Notes</div>
</div>
""", unsafe_allow_html=True)
st.markdown(f"*Last updated: {datetime.now().strftime('%B %d, %Y')}*")

st.markdown("""
<div style="background:rgba(33,150,243,0.06); border-radius:10px; padding:24px 28px; margin-bottom:16px;">
    <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">MARKET THESIS</div>
    <div style="font-size:13px; color:#999; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Core Thesis</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
         The war ended June 19 with MOU signing in Geneva. Brent fell to $83 on the announcement — down 28% from the $115 war peak, but still 18% above pre-war levels. The market has validated the L-shaped plateau thesis: Feb 2027 Brent futures settled at $80 on deal day. The structural damage — Kharg Island, South Pars, shipping insurance, SPR refill demand, Iran's legitimized Hormuz management — outlasts the political agreement by years. The $70 world required a free Hormuz. That Hormuz is gone permanently. The new floor is $80.
        The market is pricing a deal that has not yet been signed.
        A 60-day MOU draft is done: Hormuz reopens toll-free, Iran clears mines, US lifts blockade, nuclear enrichment moratorium.
        Trump has not signed. Both sides are still trading strikes while negotiating.
        Even in the full resolution scenario, Wood Mackenzie puts Brent at $80 by year-end — not $70.
        The structural damage — Kharg Island, South Pars, shipping insurance, SPR refill demand — outlasts any political agreement.
        The $70 world required a free Hormuz. That Hormuz is gone permanently.
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
    <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:10px;">Analyst View — July 26, 2026</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
        The MOU is collapsing.
        Five weeks after the June 19 Geneva signing,
        US-Iran military exchanges have resumed,
        Brent is back at $86,
        and the central question that started the war —
        what happens to Iran's nuclear program —
        remains as unresolved as it was on February 28.
        <br><br>
        The nuclear inspection dispute is the clearest signal yet
        that the MOU was a face-saving formula, not a real resolution.
        Vance declared IAEA access to Iran's bombed nuclear sites
        'a major milestone' on June 21.
        Iran denied ever agreeing to this two days later.
        Both cannot be true.
        One side misrepresented the terms,
        or both sides agreed to deliberately ambiguous language
        knowing the dispute would surface later.
        Either scenario means the 60-day window
        will not produce a permanent deal.
        The clock expires mid-August.
        <br><br>
        Goldman's scenario analysis now defines the range.
        If exports only gradually recover and Hormuz
        never fully reopens: Brent exceeds $130 by year-end.
        If Hormuz reopens quickly and demand losses persist:
        Brent at $60 in 2027.
        Today's $86 sits between these two outcomes —
        the market is pricing genuine uncertainty,
        not a resolution.
        <br><br>
        The L-shaped plateau thesis has been validated
        not once but twice.
        On June 15, Brent Feb 2027 futures settled at $80
        even as spot prices fell on the MOU announcement.
        Now in late July, spot Brent has snapped back to $86
        within five weeks of the deal.
        The market has tried to price a resolution twice.
        Both times it discovered the resolution was incomplete.
        Hochstein said it in May and it remains the most accurate
        single sentence about this conflict:
        Iranians will control Hormuz for the foreseeable future,
        it doesn't even matter what the deal says.
        The $70 world is gone.
        The question now is whether we get $86 or $130.
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
    st.caption(f"Average score: **{us_avg:.1f} / 10** &nbsp;·&nbsp; {len(us_dimensions)} dimensions &nbsp;·&nbsp; July 26, 2026")
    render_war_will(us_dimensions, "#378ADD")

with col2:
    ir_avg = sum(d["score"] for d in iran_dimensions) / len(iran_dimensions)
    st.markdown(f"### 🇮🇷 Iran")
    st.caption(f"Average score: **{ir_avg:.1f} / 10** &nbsp;·&nbsp; {len(iran_dimensions)} dimensions &nbsp;·&nbsp; July 26, 2026")
    render_war_will(iran_dimensions, "#E24B4A")