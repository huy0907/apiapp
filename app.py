from flask import Flask
from sklearn.externals import joblib
import numpy as np
from flask import request, jsonify
import pandas as pd
pipeline = joblib.load('transform_predict.joblib')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>twenty twenty API</h1>
    <p>API key: da677dc0-d3a1-4087-8754-c374a029f5b4</p>'''


@app.route('/api-real-estate-analyst', methods=['GET'])
def api_real_estate_analyst():
    # Check if API key is provides as part of URL.
    if 'apiKey' not in request.args:
        return jsonify(code=401, message="API key not found")
    else:
        # If API key is provided, assign it to a variable.
        apiKey = request.args['apiKey']
        # Check if API key is right or wrong
        if apiKey != 'da677dc0-d3a1-4087-8754-c374a029f5b4':
            return jsonify(code=401, message="Your API key is invalid or incorrect")
        else:
            # Get information from URL in here
            # Example:
            # if 'district' in request.args:
            #     district = request.args['district']
            # if 'bedroom' in request.args:
            #     bedroom = request.args['bedroom']
            props = ['district', 'bedroom', 'toilet',
                     'bathroom', 'acreage', 'houseDirection', 'balconyDirection']
            input = {}
            for i in props:
                try:
                    input[i] = request.args[i]
                except:
                    pass
            # Dự đoán giá ở đây
            #a = pd.DataFrame(['Nam', 60, 1, 2,'Bắc', 'Cầu Giấy', 55.432465], columns=['direction', 'square', 'toilet', 'bedroom', 'balcony_direction', 'district', 'center_dis'])
            df2 = pd.DataFrame(np.array([['Nam', 60, 1, 2,'Bắc', 'Cầu Giấy', 55.432465]]),columns=['direction', 'square', 'toilet', 'bedroom', 'balcony_direction', 'district', 'center_dis'])
            price =  np.exp(pipeline.predict(df2))[0]
            #result = {'money': np.exp(pipeline.predict(a))[0]}
            result = {'money' : price}
            
            # Use the jsonify function from Flask to convert our list of
            # Python dictionaries to the JSON format.
            return jsonify(code=200, message="success", content=result)

    return jsonify()