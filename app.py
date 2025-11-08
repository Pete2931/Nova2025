import pandas as pd
import streamlit as st
import prediction

st.title("Title")

# Instructions 
st.header("Welcome to Title:")
st.write("insert instructions here lol")

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
    edited_df = st.data_editor(df, column_config={"Feature": st.column_config.TextColumn("Feature", disabled=True), "Value": st.column_config.NumberColumn("Value"),}, hide_index = True, width = "content")

with col2: 
    # Prognosis 
    st.header("Prognosis")
    st.write("Normal")

    # Statistics 
    st.header("Model Statistics: ")
    cc1, cc2 = st.columns(2)
    
    with cc1: 
        st.write("Accuracy: 94.6%")
    
    with cc2: 
        st.subheader("Confusion Matrix")