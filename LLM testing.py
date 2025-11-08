import Model_Prediction as mp
import pandas as pd

data = {
    'Feature' : ['baseline_value','accelerations','fetal_movement','uterine_contractions','light_decelerations','severe_decelerations','prolongued_decelerations','abnormal_short_term_variability','mean_value_of_short_term_variability','percentage_of_time_with_abnormal_long_term_variability','mean_value_of_long_term_variability','histogram_width','histogram_min','histogram_max','histogram_number_of_peaks','histogram_number_of_zeroes','histogram_mode','histogram_mean','histogram_median','histogram_variance','histogram_tendency'],
    'Values' : [120,0.0,0,0,0,0,0,73,0.5,43,2.4,64,62,126,2,0,120,137,121,73,1]
}

df = pd.DataFrame(data)

print(mp.get_prediction(df))
print(mp.llm_explanation(df,2))