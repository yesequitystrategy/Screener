import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Sector Comparison",
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
# HELPERS
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

st.title("📊 Sector Comparison Dashboard")

# ==================================
# FILTER
# ==================================

sector = st.sidebar.selectbox(
    "Select Sector",
    sorted(df["Sector"].dropna().unique())
)

sector_df = df[
    df["Sector"] == sector
].copy()

# ==================================
# CALCULATIONS
# ==================================

sector_df["Market Cap (₹ Cr)"] = (
    sector_df["Market Cap"] / 10
)

sector_df["Revenue CAGR (%)"] = sector_df.apply(
    lambda x: calc_cagr(
        x["Sales - FY27"],
        x["Sales - FY29"]
    ),
    axis=1
)

sector_df["EBITDA CAGR (%)"] = sector_df.apply(
    lambda x: calc_cagr(
        x["EBITDA - FY27"],
        x["EBITDA - FY29"]
    ),
    axis=1
)

sector_df["PAT CAGR (%)"] = sector_df.apply(
    lambda x: calc_cagr(
        x["PAT - FY27"],
        x["PAT - FY29"]
    ),
    axis=1
)

sector_df["FY29 EBITDA Margin (%)"] = (
    sector_df["EBITDA Margin - FY29"]
)

sector_df["FY28 PE (x)"] = (
    sector_df["Fwd PE - FY28"]
)

# ==================================
# TABLE
# ==================================

comparison_df = sector_df[
    [
        "Name",
        "Market Cap (₹ Cr)",
        "Revenue CAGR (%)",
        "EBITDA CAGR (%)",
        "PAT CAGR (%)",
        "FY29 EBITDA Margin (%)",
        "FY28 PE (x)"
    ]
].copy()

comparison_df = comparison_df.sort_values(
    by="PAT CAGR (%)",
    ascending=False
)

comparison_df["Market Cap (₹ Cr)"] = (
    comparison_df["Market Cap (₹ Cr)"]
    .round(0)
    .map("{:,.0f}".format)
)

comparison_df["Revenue CAGR (%)"] = (
    comparison_df["Revenue CAGR (%)"]
    .round(1)
)

comparison_df["EBITDA CAGR (%)"] = (
    comparison_df["EBITDA CAGR (%)"]
    .round(1)
)

comparison_df["PAT CAGR (%)"] = (
    comparison_df["PAT CAGR (%)"]
    .round(1)
)

comparison_df["FY29 EBITDA Margin (%)"] = (
    comparison_df["FY29 EBITDA Margin (%)"]
    .round(1)
)

comparison_df["FY28 PE (x)"] = (
    comparison_df["FY28 PE (x)"]
    .round(1)
)

st.subheader(f"{sector} Sector Comparison")

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

# ==================================
# PE vs PAT CAGR
# ==================================

st.markdown("---")
st.subheader("Valuation vs Growth")

scatter_df = sector_df.copy()

fig = px.scatter(
    scatter_df,
    x="FY28 PE (x)",
    y="PAT CAGR (%)",
    text="Name",
    size="Market Cap (₹ Cr)",
    hover_name="Name",
    title="PE vs PAT CAGR"
)

fig.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# MARKET CAP vs REVENUE CAGR
# ==================================

st.markdown("---")
st.subheader("Market Cap vs Revenue Growth")

fig2 = px.scatter(
    sector_df,
    x="Market Cap (₹ Cr)",
    y="Revenue CAGR (%)",
    text="Name",
    size="Market Cap (₹ Cr)",
    hover_name="Name",
    title="Market Cap vs Revenue CAGR"
)

fig2.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==================================
# TOP GROWERS
# ==================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    top_pat = sector_df.sort_values(
        "PAT CAGR (%)",
        ascending=False
    )[["Name", "PAT CAGR (%)"]]

    st.subheader("Top PAT CAGR")

    st.dataframe(
        top_pat.head(5),
        use_container_width=True,
        hide_index=True
    )

with col2:

    top_margin = sector_df.sort_values(
        "FY29 EBITDA Margin (%)",
        ascending=False
    )[["Name", "FY29 EBITDA Margin (%)"]]

    st.subheader("Top EBITDA Margin")

    st.dataframe(
        top_margin.head(5),
        use_container_width=True,
        hide_index=True
    )