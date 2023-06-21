%%writefile webapp.py
from flask import Flask, request
import pandas as pd
#from keras.models import load_model
from function import detect_anomaly, load_model

app = Flask(__name__)

# Load the pre-trained Keras model
model = load_model('lstm_final_adam_50e')

@app.route('/', methods=['GET'])
def index():
 return "Hello, world!"

@app.route('/prediction', methods=['POST'])
def predict():
    # Get the uploaded file from the request
    file = request.files['file']

    # Read the CSV file into a DataFrame
    # df = pd.read_csv(file)
    # print(df)

    # cols = list(pd.read_csv(file, nrows=1))

    # data = pd.read_csv(file,
    #            usecols =[i for i in cols if i != 'dst_ip' and i != 'FID' 
    #                      and i != 'SimillarHTTP' and i != 'Unnamed: 0' and i != ' Inbound'])
    # print(data)
    
    json_result = detect_anomaly(file, model)

    # Preprocess the data if needed
    # ...

    # Run the prediction
    # prediction = model.predict(df)

    # Process the prediction results if needed
    # ...

    # Return the prediction as a response
    # response = {
    #     'prediction': prediction.tolist()
    # }
    # return jsonify(response)
    # return df.to_string()
    return json_result

if __name__ == '__main__':
    app.run(port=5005)
