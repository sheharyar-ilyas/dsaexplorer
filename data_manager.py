from pathlib import Path
import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).resolve().parent / "data" / "dataset.csv"


@st.cache_data(show_spinner="Loading dataset...")
def get_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_FILE}. "
        )

    return pd.read_csv(DATA_FILE)


def get_dataset_info():
    df = get_data()
    return {
        "rows": len(df),
        "columns": len(df.columns),
    }