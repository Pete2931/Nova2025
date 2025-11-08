import json
import pandas
import xgboost as xgb
from xgboost import XGBClassifier
import numpy as np
import requests
import base64

openrouter_api_key_file = open("OPENROUTER_API_KEY.txt", 'r')
openrouter_api_key = openrouter_api_key_file.read() # This is your API key to use in requests
openrouter_api_key_file.close()

#This is to transform the data given by front-end to be ready for prediction
def transfrom_dataframe(df):
    return df.set_index('Feature').T

#Predicting the patient, returns 0,1,2
def prediction(data):
    model = XGBClassifier()
    model_path = "xgb_model.json"
    model.load(model_path)
    return model.predict(data)[0]

#For front_end to call to: returns Normal, Suspected, Pathological
def get_prediction(df):
    code = ['Normal','Suspect','Pathological']
    res = prediction(transfrom_dataframe(df))
    return code[res]

#Function encodes an image to base 64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')