import streamlit as st
import pandas as pd

def load_tables():
    # Load CSVs
    cm = pd.read_csv("confusion_matrix.csv", index_col=0)
    cr = pd.read_csv("classification_report.csv", index_col=0)

    # Convert numeric columns
    cr = cr.apply(pd.to_numeric, errors="ignore")

    # Make accuracy show only one value (in the f1-score column)
    if "accuracy" in cr.index:
        acc_val = cr.loc["accuracy", "f1-score"]
        cr.loc["accuracy"] = ["", "", acc_val, ""]

    # Convert numeric values to percentage (2 decimals)
    for col in cr.columns:
        cr[col] = cr[col].apply(
            lambda x: f"{x*100:.2f}%" if isinstance(x, (int, float)) and x <= 1.0 else
            (f"{x:.0f}" if isinstance(x, (int, float)) else x)
        )

    # Display both tables
    st.dataframe(cm)
    st.dataframe(cr)