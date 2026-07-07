import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    file_path = "data/Consensus Sheet1 - TEST.xlsb"

    df = pd.read_excel(
        file_path,
        sheet_name="Auto",
        engine="pyxlsb"
    )

    df.columns = df.columns.str.strip()

    return df