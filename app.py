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

total_score = round((10 + 9 + 6 + 4) / 4, 1)
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
        <div style="font-size:13px; font-weight:700; color:#4a9fd4; letter-spacing:3px; text-transform:uppercase; margin-bottom:10px;">
            CRUDE OIL POLICY & EVENT RISK DASHBOARD
        </div>
        <div style="font-size:56px; font-weight:900; color:#ffffff; letter-spacing:-2px; line-height:1; margin-bottom:6px;">
            COPE Index
        </div>
        <div style="font-size:13px; color:#7aa3c0; margin-top:14px; padding-top:14px; border-top:1px solid rgba(255,255,255,0.1);">
            Tracking how geopolitical events and policy signals translate into crude oil price risk
            &nbsp;·&nbsp;
            Last updated: {datetime.now().strftime('%B %d, %Y %H:%M')} ET
        </div>
    </div>
    <div style="display:flex; gap:32px; margin-left:48px;">
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#7aa3c0; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">Brent Crude</div>
            <div style="font-size:32px; font-weight:800; color:#ffffff;">{wti_str}</div>
            <div style="font-size:13px; color:{wti_color}; margin-top:4px;">{wti_chg_str} vs prev day</div>
        </div>
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#7aa3c0; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">COPE Risk Score</div>
            <div style="font-size:32px; font-weight:800; color:{risk_color};">{total_score:.1f}/10</div>
            <div style="font-size:13px; color:{risk_color}; margin-top:4px;">{risk_label}</div>
        </div>
        <div style="text-align:center; padding:20px 28px; background:rgba(255,255,255,0.06); border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:11px; color:#7aa3c0; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">Hormuz Status</div>
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
        "note": "US-Israel strikes began Feb 28. Khamenei assassinated. Kharg Island — Iran's main oil export hub handling 90% of exports — struck by US forces. Hormuz near standstill."
    },
    "Middle East Conflict Risk": {
        "score": 9, "trend": "↑",
        "note": "Active war theater. Houthi, Iraqi militia, Hezbollah all activated. Regional spillover risk at highest level since 2003."
    },
    "Russia Supply Disruption": {
        "score": 6, "trend": "→",
        "note": "Ukraine conflict continues. Russian exports rerouted to Asia but volumes stable."
    },
    "US Energy Policy Uncertainty": {
        "score": 4, "trend": "→",
        "note": "IEA 400mb stockpile release underway"
    }
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

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

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

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块三
# ══════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_dxy_data():
    ticker = yf.Ticker("DX=F")
    df = ticker.history(start="2000-01-01")[["Close"]].reset_index()
    df.columns = ["date", "dxy"]
    df["date"] = df["date"].apply(lambda x: x.replace(tzinfo=None) if hasattr(x, 'tzinfo') else x)
    df["dxy"] = pd.to_numeric(df["dxy"], errors="coerce")
    df = df.dropna()
    return df

st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">💵 US Dollar Index (DXY)</div>
</div>
""", unsafe_allow_html=True)
st.markdown("A stronger dollar typically pressures oil prices lower — dollar and crude move inversely.")
st.caption("Source: Yahoo Finance")

try:
    dxy = load_dxy_data()
    wti_df, brent_df = load_price_data()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wti_df["date"], y=wti_df["wti"], mode="lines", name="WTI (USD/bbl)",
        line=dict(color="#2196F3", width=1.5), yaxis="y1"))
    fig.add_trace(go.Scatter(x=dxy["date"], y=dxy["dxy"], mode="lines", name="DXY Index",
        line=dict(color="#f59e0b", width=1.5), yaxis="y2"))
    fig.update_layout(height=480, hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(title="WTI (USD/bbl)", gridcolor="rgba(128,128,128,0.15)"),
        yaxis2=dict(title="DXY", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
        margin=dict(t=40, b=20, r=80))
    st.plotly_chart(fig, use_container_width=True)

    dxy_latest = float(dxy["dxy"].iloc[-1])
    dxy_prev = float(dxy["dxy"].iloc[-2])
    dxy_change = dxy_latest - dxy_prev
    dxy_1y_mean = float(dxy["dxy"].tail(252).mean())
    dxy_vs_mean = "above" if dxy_latest > dxy_1y_mean else "below"

    dxy_30 = dxy.tail(30).set_index("date")["dxy"]
    wti_30 = wti_df.tail(30).set_index("date")["wti"]
    merged = pd.merge(dxy_30.reset_index(), wti_30.reset_index(), on="date")
    corr = merged["dxy"].corr(merged["wti"])

    if dxy_change < -0.3:
        day_signal, dollar_word, oil_signal = "fell", "weakening", "bullish for oil prices"
    elif dxy_change > 0.3:
        day_signal, dollar_word, oil_signal = "rose", "strengthening", "bearish for oil prices"
    else:
        day_signal, dollar_word, oil_signal = "was stable", "stable", "neutral for oil prices"

    line1 = "DXY {} {:+.2f} today to {:.2f}, currently {} its 1-year average ({:.2f}) — a {} dollar is typically {}.".format(
        day_signal, dxy_change, dxy_latest, dxy_vs_mean, dxy_1y_mean, dollar_word, oil_signal)

    if corr > 0.3:
        box_bg, box_border = "#fffbeb", "#f59e0b"
        corr_title_color = "#92400e"
        corr_title = "⚠️ 30-Day DXY/WTI Correlation: {:.2f} — Traditional inverse relationship has broken down".format(corr)
        corr_body = "Hormuz closure has become the dominant price driver. The traditional DXY-oil inverse relationship no longer applies — geopolitics, not the dollar, is setting the price."
    elif corr < -0.3:
        box_bg, box_border = "#f0fdf4", "#22c55e"
        corr_title_color = "#166534"
        corr_title = "✅ 30-Day DXY/WTI Correlation: {:.2f} — Inverse relationship intact".format(corr)
        corr_body = "DXY remains a reliable leading indicator. Dollar strength/weakness is transmitting normally into oil prices."
    else:
        box_bg, box_border = "#f8fafc", "#94a3b8"
        corr_title_color = "#475569"
        corr_title = "➡️ 30-Day DXY/WTI Correlation: {:.2f} — Decoupled".format(corr)
        corr_body = "DXY and oil are temporarily decoupled. Other factors are dominating price direction."

    st.markdown(
        "<div style='background:" + box_bg + "; border-left:4px solid " + box_border + "; border-radius:6px; padding:20px 24px; margin-bottom:20px;'>"
        "<div style='font-size:15px; color:#333; margin-bottom:10px;'>" + line1 + "</div>"
        "<div style='font-size:17px; font-weight:700; color:" + corr_title_color + "; margin-bottom:10px;'>" + corr_title + "</div>"
        "<div style='font-size:14px; color:#555; line-height:1.7;'>" + corr_body + "</div>"
        "</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DXY Latest", f"{dxy_latest:.2f}", f"{dxy_change:+.2f} vs prev day")
    with col2:
        st.metric("DXY vs 1-Year Average", f"{dxy_1y_mean:.2f} avg", f"Currently {dxy_vs_mean} average")
    with col3:
        st.metric("30-Day Correlation", f"{corr:.2f}", "Positive = relationship broken" if corr > 0.3 else "Inverse intact")

except Exception as e:
    st.error(f"Error loading DXY data: {e}")

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# 模块四
# ══════════════════════════════════════════
st.markdown("""
<div style="border-left:4px solid #1a6faf; padding-left:12px; margin:24px 0 8px 0;">
    <div style="font-size:22px; font-weight:700;">⚙️ Market Indicators — Supply Buffer & Demand Signal</div>
</div>
""", unsafe_allow_html=True)
st.markdown("Tracking emergency supply response to the Hormuz closure, and demand-side signals from the world's largest crude importer.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:rgba(33,150,243,0.05); border-radius:10px; padding:20px 24px;">
        <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">EIA Weekly Inventory Change</div>
        <div style="font-size:13px; color:#999; margin-bottom:16px;">US crude oil stockpile — weekly change reported by EIA</div>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data(ttl=86400)
    def fetch_eia_inventory():
        url = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"
        params = {
            "api_key": "da8td88uyU2zNniqDR7g9CoiEwmnGT8fOXbO5Tt9",
            "frequency": "weekly", "data[0]": "value",
            "facets[product][]": "EPC0", "facets[duoarea][]": "NUS",
            "facets[process][]": "SAE", "sort[0][column]": "period",
            "sort[0][direction]": "desc", "length": 10
        }
        response = requests.get(url, params=params)
        data = response.json()
        records = data.get("response", {}).get("data", [])
        df = pd.DataFrame(records)
        df["period"] = pd.to_datetime(df["period"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.sort_values("period").reset_index(drop=True)
        df["change_mb"] = df["value"].diff() / 1000
        return df

    try:
        eia_df = fetch_eia_inventory()
        recent = eia_df.dropna(subset=["change_mb"]).tail(6)
        if not recent.empty:
            latest_change = recent.iloc[-1]["change_mb"]
            latest_date = recent.iloc[-1]["period"].strftime("%b %d, %Y")
            direction = "Bullish draw" if latest_change < 0 else "Bearish build"
            st.metric(label=f"Latest Week ({latest_date})", value=f"{latest_change:+.1f} mb", delta=direction)
            st.caption("A surprise draw is bullish for prices — less supply than expected.")
            fig_bar = go.Figure(go.Bar(
                x=recent["period"].dt.strftime("%b %d"), y=recent["change_mb"],
                marker_color=["#22c55e" if x < 0 else "#ef4444" for x in recent["change_mb"]]))
            fig_bar.update_layout(height=260, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="rgba(128,128,128,0.15)", title="Million Barrels"), margin=dict(t=10, b=10))
            st.plotly_chart(fig_bar, use_container_width=True)
    except Exception as e:
        st.error(f"EIA API error: {e}")

with col2:
    st.markdown("""
    <div style="background:rgba(239,68,68,0.05); border-radius:10px; padding:20px 24px;">
        <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">IEA Emergency Reserve Release</div>
        <div style="font-size:13px; color:#999; margin-bottom:16px;">Coordinated global strategic reserve release — March 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.metric(label="Total Pledged (Mar 11, 2026)", value="400 mb", delta="Largest release in IEA history")
    st.metric(label="US SPR Contribution", value="172 mb", delta="~120 days to fully deliver")
    st.caption("Source: IEA press release Mar 11, 2026 · Bloomberg")

    st.markdown("""
    <div style="background:rgba(239,68,68,0.06); border-left:3px solid #ef4444; border-radius:6px; padding:16px 18px; margin-top:16px;">
        <div style="font-size:15px; font-weight:700; color:#ef4444; margin-bottom:10px;">⚠️ Why oil prices haven't fallen</div>
        <div style="font-size:14px; color:#555; line-height:1.8;">
            IEA release rate: <strong>~6.7 mb/d</strong><br>
            Hormuz closure impact: <strong>~20 mb/d</strong><br>
            Unmet gap: <strong>~13 mb/d per day</strong>
        </div>
        <div style="font-size:13px; color:#888; margin-top:10px; line-height:1.6;">
            The release covers only ~33% of the daily supply loss.
            Physical barrels cannot reach markets while Hormuz remains closed —
            the buffer exists on paper, but not in the pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(148,163,184,0.08); border-radius:10px; padding:20px 24px; margin-bottom:8px;">
    <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">China Manufacturing PMI — Demand Signal</div>
    <div style="font-size:13px; color:#999;">Demand-side weakness currently overridden by Hormuz supply shock</div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1, 1])
with col3:
    st.metric(label="Feb 2026 PMI", value="49.0", delta="-0.3 vs Jan (Contracting)")
    st.caption("PMI >50 = expansion. China is the world's largest crude importer.")
    st.markdown("""
    <div style="background:rgba(148,163,184,0.1); border-left:3px solid #94a3b8; border-radius:6px; padding:14px 16px; margin-top:12px;">
        <div style="font-size:14px; color:#555; line-height:1.7;">
            China PMI has been <strong>below 50 for 6 consecutive months</strong> — demand-side weakness that would normally suppress oil prices.
            <br><br>
            Currently <strong>overridden by the Hormuz supply shock</strong>. Even with contracting Chinese demand, prices remain elevated above $90/bbl.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pmis = pd.DataFrame({"month": ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"], "pmi": [49.5, 49.7, 49.3, 49.4, 49.3, 49.0]})
    fig_pmi = go.Figure()
    fig_pmi.add_trace(go.Scatter(x=pmis["month"], y=pmis["pmi"], mode="lines+markers",
        line=dict(color="#2196F3", width=2), marker=dict(size=8)))
    fig_pmi.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="50 = Neutral")
    fig_pmi.update_layout(height=220, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.15)", range=[48, 53]), margin=dict(t=10, b=10))
    st.plotly_chart(fig_pmi, use_container_width=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

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
    open_kw = ["open", "resume", "reopen", "pass", "transit", "allowing", "escort", "sneak"]
    open_hits = [a for a in hormuz_evidence if any(k in a["title_lower"] for k in open_kw)]
    hormuz_status = "🟡 Partial Recovery Signals" if len(open_hits) >= 2 else "🔴 Effectively Closed"
    hormuz_color = "#f59e0b" if len(open_hits) >= 2 else "#ef4444"

    # ── 手动更新 — 每天根据新闻判断修改下面四行
    war_signal = "🔴 Escalation Intensifying — Leadership Targeting Continues"
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
        {"title": "🟢 Scenario A: Hormuz Reopens within 30 Days", "direction": "Sharply Bearish",
         "driver": "Geopolitical risk premium collapses as tanker traffic resumes. IEA emergency reserves wind down. Pre-war demand fundamentals reassert. Demand destruction from elevated prices adds further downward pressure. Expect a rapid, significant price correction.",
         "bg": "rgba(34,197,94,0.06)", "border": "#22c55e", "color": "#166534", "dir_color": "#22c55e"},
        {"title": "🟡 Scenario B: Partial Resolution — 60 to 90 Days", "direction": "Neutral with High Volatility",
         "driver": "Ceasefire negotiations begin but Hormuz only partially reopens. IEA reserve release (~6.7 mb/d) provides partial buffer against the ~20 mb/d supply gap. Market remains caught between supply disruption and demand destruction. High volatility, no clear directional trend.",
         "bg": "rgba(245,158,11,0.06)", "border": "#f59e0b", "color": "#92400e", "dir_color": "#f59e0b"},
        {"title": "🔴 Scenario C: Closure Extends Beyond 90 Days", "direction": "Bullish — Upside Risk Dominant",
         "driver": "Supply deficit compounds week over week. IEA reserves insufficient to close ~13 mb/d daily gap. Demand destruction accelerates as recession risk rises in Europe and Asia. Iranian political vacuum after Khamenei assassination prolongs conflict. Upside risk remains the dominant force.",
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

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

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
        "date": "Mar 17, 2026",
        "action": "Israel kills Iran security chief Larijani and Basij commander Soleimani — confirmed by Iran",
        "interpretation": "Most significant leadership killing since Khamenei on Feb 28. Larijani was Iran's top security official and lead nuclear negotiator — his death deepens Iran's political vacuum and makes near-term ceasefire negotiations far less likely. Bullish signal — Hormuz reopening timeline extends further.",
        "impact": "🔺 Bullish",
        "source_title": "Israel kills Iran's security chief Larijani and Basij commander — Al Jazeera",
        "source_url": "https://www.aljazeera.com/news/2026/3/17/israel-says-it-has-killed-ali-larijani-irans-top-security-official"
    },
    {
        "date": "Mar 17, 2026",
        "action": "Hassett signals conflict will end in 4–6 weeks — markets skeptical",
        "interpretation": "White House economic adviser Hassett told markets the Iran conflict would be over in 4–6 weeks. Markets briefly rallied, but oil simultaneously rose as Iranian strikes on Gulf infrastructure escalated. The contradiction tells you the market does not believe this timeline. If credible, front-month futures would price this in immediately — sharp downside volatility would follow even before formal ceasefire.",
        "impact": "🟡 Neutral",
        "source_title": "Hassett signals conflict ends in weeks — Wall Street CN",
        "source_url": "https://wallstreetcn.com/articles/3767701"
    },
    {
        "date": "Mar 16, 2026",
        "action": "Trump pressures China and NATO to help open Hormuz — no concrete enforcement mechanism announced",
        "interpretation": "Neutral to slightly bullish. Diplomatic pressure without military backing is unlikely to move Iran. If China complies, could accelerate reopening timeline — but no evidence of Chinese cooperation yet. Markets are not pricing this in.",
        "impact": "🟡 Neutral",
        "source_title": "Iran War Live Updates: Trump Pressures China and NATO — NYT",
        "source_url": "https://www.nytimes.com"
    },
    {
        "date": "Mar 13, 2026",
        "action": "Russia oil sanctions partially eased — stranded cargoes allowed to trade",
        "interpretation": "Short-term bearish signal. Allows ~1-2 mb/d of previously stranded Russian oil back into the market. However, impact is limited — volumes are small relative to the ~20 mb/d Hormuz disruption, and the move faces pushback from G7 allies.",
        "impact": "🔻 Bearish",
        "source_title": "US easing of Russia oil sanctions faces pushback — BBC",
        "source_url": "https://www.bbc.com"
    },
    {
        "date": "Mar 11, 2026",
        "action": "Trump announces US SPR release — 172mb over 120 days (~1.4 mb/d)",
        "interpretation": "Marginally bearish but largely symbolic. At 1.4 mb/d, the US SPR contribution is the smallest component of the IEA release. The 120-day delivery timeline means oil won't hit the market quickly enough to offset the immediate supply shock.",
        "impact": "🔻 Bearish",
        "source_title": "US to Release 172 Million Barrels From SPR — Bloomberg",
        "source_url": "https://www.bloomberg.com"
    },
    {
        "date": "Mar 11, 2026",
        "action": "IEA 400mb emergency reserve release coordinated with G7",
        "interpretation": "Bearish on paper, but insufficient in practice. Release rate (~6.7 mb/d) covers only ~33% of the daily Hormuz supply gap (~20 mb/d). Markets initially sold off on the news but quickly recovered as traders recognized the arithmetic.",
        "impact": "🔻 Bearish",
        "source_title": "IEA agrees to release record 400 million barrels — Al Jazeera",
        "source_url": "https://www.aljazeera.com"
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
            Net policy impact is <strong>marginally bearish</strong> — SPR release and Russia sanctions easing add supply on paper.
            But all measures combined cover less than 50% of the Hormuz supply gap.
            <br><br>
            The dominant variable remains the war itself — not White House policy.
            Watch for any shift in Trump's position on Iran negotiations as the key policy catalyst.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1px; background:linear-gradient(to right, #1a6faf, transparent); margin:32px 0;'></div>", unsafe_allow_html=True)

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
    <div style="font-size:20px; font-weight:800; color:#1a1a1a; margin-bottom:4px;">MARKET THESIS — March 17, 2026</div>
    <div style="font-size:13px; color:#999; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Core Thesis</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
        Brent is trading near $100/bbl in an environment of extreme policy noise and unresolved supply disruption.
        Hassett signaled the conflict could end in 4–6 weeks — markets rallied briefly, but oil prices rose simultaneously as Iranian strikes on Gulf infrastructure escalated.
        This contradiction tells you everything: the market does not believe the war is ending soon.
        The Hormuz closure remains the single dominant force — DXY, China PMI, IEA reserves are all secondary until tanker traffic resumes.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background:rgba(239,68,68,0.08); border-left:3px solid #ef4444; border-radius:6px; padding:16px 18px;">
        <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:12px;">🔺 Key Upside Risks</div>
        <div style="font-size:14px; color:#444; line-height:2.0;">
            • Hormuz remains closed — every additional week compounds the supply deficit<br>
            • Iranian political vacuum after Khamenei assassination prolongs conflict<br>
            • Escalating strikes on Gulf infrastructure (Kharg Island, Qatar LNG)<br>
            • Red Sea alternative route also under threat — no viable bypass at scale<br>
            • Stagflation risk — central banks forced to choose between growth and inflation
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:rgba(34,197,94,0.08); border-left:3px solid #22c55e; border-radius:6px; padding:16px 18px;">
        <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:12px;">🔻 Key Downside Risks</div>
        <div style="font-size:14px; color:#444; line-height:2.0;">
            • Ceasefire/negotiated settlement — prices could drop $20–30/bbl within days<br>
            • Hassett "4–6 weeks" timeline — front-month futures will price this in immediately if credible<br>
            • IEA reserve release provides partial short-term supply buffer<br>
            • Demand destruction — high prices already slowing global economy<br>
            • US shale response accelerating — rig count rising<br>
            • Fed hawkish pivot — rate hikes to combat oil-driven inflation could suppress demand
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(26,111,175,0.1); border-left:4px solid #1a6faf; border-radius:6px; padding:18px 20px; margin-top:16px;">
    <div style="font-size:16px; font-weight:800; color:#1a1a1a; margin-bottom:10px;">Analyst View — March 17, 2026</div>
    <div style="font-size:15px; color:#444; line-height:1.8;">
        Watch Hormuz tanker traffic as the single most important indicator —
        any confirmed passage of loaded tankers would be the clearest bullish-to-bearish reversal signal.
        Hassett's 4–6 week timeline is the new key variable: if the market begins to price this in,
        expect sharp downside volatility even before the war formally ends.
        Until then, upside risk remains dominant.
    </div>
</div>
""", unsafe_allow_html=True)