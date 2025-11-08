import pandas as pd
import streamlit as st
import confusion_classificationTables
import Model_Prediction

st.set_page_config(layout="wide", page_title="FetoScope")

st.title("FetoScope")

# Instructions 
st.header("Welcome to FetoScope:")
st.subheader("To use this dashboard:")
st.write("**1. Enter CTG Values**")
st.write("Fill in each field in the table on the left using the readings from the cardiotocograph.")
st.write("**2. Run the analysis**")
st.write("After all required fields are filled, the model will train/evaluate and generate a prediction.")
st.write("**3. Review the results on the right panel**")
st.write("The Prognosis panel presents the model's fetal health prediction—Normal, Suspect, or Pathological—and summarizes how trustworthy that prediction is with key performance metrics (accuracy, precision, recall, F1). Beneath the scores, you'll also see a clear, plain-language explanation highlighting the most influential features from your CTG inputs and why they pushed the model toward its conclusion.")


# Input Data
features = ["baseline_value","accelerations","fetal_movement","uterine_contractions","light_decelerations","severe_decelerations","prolongued_decelerations","abnormal_short_term_variability","mean_value_of_short_term_variability","percentage_of_time_with_abnormal_long_term_variability","mean_value_of_long_term_variability","histogram_width","histogram_min","histogram_max","histogram_number_of_peaks","histogram_number_of_zeroes","histogram_mode","histogram_mean","histogram_median","histogram_variance","histogram_tendency"]

df = pd.DataFrame({"Feature": features, "Value": [0]*len(features)})

col1, col2 = st.columns(2, gap = "large")


with col1: 
    st.header("Input Data")
    with st.form("ctg_form"):
        edited_df = st.data_editor(df, column_config={"Feature": st.column_config.TextColumn("Feature", disabled=True), "Value": st.column_config.NumberColumn("Value"),}, hide_index = True, width = "content")
        edited_df['Value'] = edited_df['Value'].astype(int)
        submitted = st.form_submit_button("Run analysis", type="primary")

label = ""
explanation = ""

if submitted: 
    label, explanation = Model_Prediction.get_pred_exp(edited_df)

with col2: 
    # Statistics 
    st.header("Model Statistics: ")
    confusion_classificationTables.load_tables()

# Prognosis 
st.header("Prognosis")
st.write(label)

st.header("Reasons for Progonsis")
if submitted:
    st.markdown(explanation)
    st.success("Analysis Complete!")