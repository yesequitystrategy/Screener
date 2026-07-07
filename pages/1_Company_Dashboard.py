import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Stock Estimates Dashboard",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "data/Consensus Sheet1 - TEST.xlsb",
        sheet_name="Auto",
        engine="pyxlsb"
    )

    df.columns = df.columns.str.strip()

    return df


# ==================================
# HELPER FUNCTIONS
# ==================================

def calc_cagr(start, end, years=2):

    if pd.isna(start) or pd.isna(end):
        return None

    if start <= 0 or end <= 0:
        return None

    return ((end / start) ** (1 / years) - 1) * 100


def mn_to_cr(value):

    if pd.isna(value):
        return None

    return value / 10


# ==================================
# LOAD DATA
# ==================================

df = load_data()

# ==================================
# TITLE
# ==================================

st.title("📈 Stock Estimates Dashboard")

# ==================================
# SIDEBAR
# ==================================

sector = st.sidebar.selectbox(
    "Select Sector",
    sorted(df["Sector"].dropna().unique())
)

stock = st.sidebar.selectbox(
    "Select Stock",
    sorted(
        df.loc[
            df["Sector"] == sector,
            "Name"
        ].dropna().unique()
    )
)

# ==================================
# COMPANY DATA
# ==================================

company = df[
    (df["Sector"] == sector)
    & (df["Name"] == stock)
]

if company.empty:
    st.warning("No data available")
    st.stop()

row = company.iloc[0]

# ==================================
# HEADER
# ==================================

st.subheader(row["Name"])

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Ticker",
        row["Ticker"]
    )

with c2:
    st.metric(
        "Market Cap (₹ Cr)",
        f"{mn_to_cr(row['Market Cap']):,.0f}"
    )

with c3:
    st.metric(
        "Sector",
        row["Sector"]
    )

# ==================================
# CAGR
# ==================================

revenue_cagr = calc_cagr(
    row["Sales - FY27"],
    row["Sales - FY29"]
)

ebitda_cagr = calc_cagr(
    row["EBITDA - FY27"],
    row["EBITDA - FY29"]
)

pat_cagr = calc_cagr(
    row["PAT - FY27"],
    row["PAT - FY29"]
)

# ==================================
# KPI SECTION
# ==================================

st.markdown("### Growth Metrics")

k1, k2, k3 = st.columns(3)

with k1:
    st.metric(
        "Revenue CAGR FY27-29",
        f"{revenue_cagr:.1f}%"
    )

with k2:
    st.metric(
        "EBITDA CAGR FY27-29",
        f"{ebitda_cagr:.1f}%"
    )

with k3:
    st.metric(
        "PAT CAGR FY27-29",
        f"{pat_cagr:.1f}%"
    )

# ==================================
# ESTIMATES TABLE
# ==================================

estimates_df = pd.DataFrame({

    "Metric": [
        "Revenue (₹ Cr)",
        "EBITDA (₹ Cr)",
        "PAT (₹ Cr)",
        "EBITDA Margin (%)",
        "Forward PE (x)"
    ],

    "FY27": [
        f"{mn_to_cr(row['Sales - FY27']):,.0f}",
        f"{mn_to_cr(row['EBITDA - FY27']):,.0f}",
        f"{mn_to_cr(row['PAT - FY27']):,.0f}",
        f"{row['EBITDA Margin - FY27']:.1f}",
        f"{row['Fwd PE - FY27']:.1f}"
    ],

    "FY28": [
        f"{mn_to_cr(row['Sales - FY28']):,.0f}",
        f"{mn_to_cr(row['EBITDA - FY28']):,.0f}",
        f"{mn_to_cr(row['PAT - FY28']):,.0f}",
        f"{row['EBITDA Margin - FY28']:.1f}",
        f"{row['Fwd PE - FY28']:.1f}"
    ],

    "FY29": [
        f"{mn_to_cr(row['Sales - FY29']):,.0f}",
        f"{mn_to_cr(row['EBITDA - FY29']):,.0f}",
        f"{mn_to_cr(row['PAT - FY29']):,.0f}",
        f"{row['EBITDA Margin - FY29']:.1f}",
        "-"
    ]
})

st.markdown("---")
st.subheader("Consensus Estimates (₹ Crore)")

st.dataframe(
    estimates_df,
    use_container_width=True,
    hide_index=True
)

# ==================================
# CHART DATA
# ==================================

revenue_df = pd.DataFrame({
    "FY": ["FY27", "FY28", "FY29"],
    "Revenue": [
        mn_to_cr(row["Sales - FY27"]),
        mn_to_cr(row["Sales - FY28"]),
        mn_to_cr(row["Sales - FY29"])
    ]
})

ebitda_df = pd.DataFrame({
    "FY": ["FY27", "FY28", "FY29"],
    "EBITDA": [
        mn_to_cr(row["EBITDA - FY27"]),
        mn_to_cr(row["EBITDA - FY28"]),
        mn_to_cr(row["EBITDA - FY29"])
    ]
})

pat_df = pd.DataFrame({
    "FY": ["FY27", "FY28", "FY29"],
    "PAT": [
        mn_to_cr(row["PAT - FY27"]),
        mn_to_cr(row["PAT - FY28"]),
        mn_to_cr(row["PAT - FY29"])
    ]
})

margin_df = pd.DataFrame({
    "FY": ["FY27", "FY28", "FY29"],
    "Margin": [
        row["EBITDA Margin - FY27"],
        row["EBITDA Margin - FY28"],
        row["EBITDA Margin - FY29"]
    ]
})

# ==================================
# CHARTS
# ==================================

st.markdown("---")
st.subheader("Financial Trends")

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        revenue_df,
        x="FY",
        y="Revenue",
        title="Revenue (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        ebitda_df,
        x="FY",
        y="EBITDA",
        title="EBITDA (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:

    fig = px.bar(
        pat_df,
        x="FY",
        y="PAT",
        title="PAT (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    fig = px.line(
        margin_df,
        x="FY",
        y="Margin",
        markers=True,
        title="EBITDA Margin (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )