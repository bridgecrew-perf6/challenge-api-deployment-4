import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from pipeline.predict.prediction import predict
# from pipeline.preprocessing.cleaning_data_vers02 import preprocess
from pipeline.preprocessing.clean_test import preprocess
import pipeline.model as model

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    function returns string on welcome page
    parameters: GET
    return: "Alive!"
    """
    return "Alive!"


@app.route('/welcome', methods=["GET"])
def welcome():
    """
    function returns string on home page
    parameters: GET
    return: "Welcome to API Deployment"
    """
    return "Welcome to API Deployment"


@app.route("/predict", methods=["POST"])
def predict_api():
    """
    function returns predicted price
    parameters: GET,POST
    return: "The predicted price is VALUE"
    """
    data = request.get_json()
    dataset = pd.DataFrame(data, index=[0, ])
    dataset.replace(True, int(1), inplace=True)
    dataset.replace(False, int(0), inplace=True)
    # dataset.replace(1.0, int(1), inplace=True)
    new_df = preprocess(dataset)

    print(type(new_df))
    if isinstance(new_df, str):
        if new_df == "Error-Missing!":
            return "Area, property-type, rooms-number or zip-code is missing"
        elif new_df == "Error-Property":
            return "Only input APARTMENT, HOUSE or OTHERS for property"
        elif new_df == "Error-ZipCode":
            return "Wrong zip-code input. Must be [1000-9998]"
    else:
        result = predict(new_df)
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
