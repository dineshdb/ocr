from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    # 1. load the template for homepage containing
    # 2. form for file upload and submit/predict button
    # 3. upload the file and save in the database
    # 4. redirect to the predict page
    # 5. use POST method to take the file

    return "This webpage contains the homepage"

@app.route('/predict')
def predict():

    # 1. get the uploaded file from database 
    # 2. get the trained model from the database
    # 3. predict the file using the model
    # 4. send predicted data to the client
    # 5. display the original image and the text

    return "This function predicts the model"

if __name__ == '__main__':
    app.run(debug=True)
