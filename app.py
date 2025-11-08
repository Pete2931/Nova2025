import pandas as pd
import streamlit as st
import confusion_classificationTables
import Model_Prediction

st.set_page_config(layout="wide", page_title="FetoScope")
st.markdown("""
<style>
.card {
  background-color: rgba(255,255,255,0.5);
  border-radius: 25px;
  padding: 18px 20px;
  margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("FetoScope")

# Instructions 
st.header("Welcome to FetoScope:")
st.subheader("To use this dashboard:")
st.write("**1. Enter CTG Values**")
st.write("Fill in each field in the table on the left using the readings from the cardiotocograph.")
st.write("**2. Run the analysis**")
st.write("After all required fields are filled, the model will train/evaluate and generate a prediction.")
st.write("**3. Review the results on the right panel**")


# Input Data
features = [
    "baseline_value","accelerations","uterine_contractions",
    "light_decelerations","severe_decelerations","prolongued_decelerations",
    "mean_value_of_short_term_variability","mean_value_of_long_term_variability",
    "histogram_width","histogram_min","histogram_max","histogram_variance"
]

df = pd.DataFrame({"Feature": features, "Value": [None]*len(features)})

col1, col2 = st.columns(2, gap = "large")

with col1: 
    st.header("Input Data")
    with st.form("ctg_form"):
        edited_df = st.data_editor(df, column_config={"Feature": st.column_config.TextColumn("Feature", disabled=True), "Value": st.column_config.NumberColumn("Value"),}, hide_index = True, width = "content")
        submitted = st.form_submit_button("Run analysis", type="primary")

with col2: 
    # Prognosis 
    st.header("Prognosis")
    st.write("Normal")

    # Statistics 
    st.header("Model Statistics: ")
    confusion_classificationTables.load_tables()

    st.header("LLM Explanation")
    if submitted:
        missing = edited_df.loc[edited_df["Value"].isna(), "Feature"].tolist()
        if missing:
            st.error(f"Missing values: {', '.join(missing)}")
        else:
            values = {r["Feature"]: r["Value"] for _, r in edited_df.iterrows()}
            result = Model_Prediction.get_pred_exp(edited_df)[1]
            st.success("Analysis complete!")