from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, Response, jsonify
from werkzeug.utils import secure_filename
import os

from predictor import find_texts

UPLOAD_FOLDER = "./public/uploads/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<path:path>')
def send_css(path):
    return send_from_directory('public', path)
    
@app.route('/')
def get_home():
    return send_from_directory('public', 'index.html')
    
@app.route('/', methods=['POST'])
def home():

    # 1. load the template for homepage containing - done
    # 2. form for file upload and submit/predict button - done
    # 3. upload the file and save in the (-database)/file - done
    # 4. use POST method to take the file - done
    # 5. Return predicted values
    # 6. Display values
    # 7. Readjust parameters for rescan

    if request.method == 'POST':

        # check if the post request has the file part
        if 'files' not in request.files:
           return Response("{'id':'" + str(request.form) + "'}", status=401, mimetype='application/json')

        file = request.files['files']
        file_id = request.form['id']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return Response("{}", status=201, mimetype='application/json')
        print(file_id, file, file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_id))
            return jsonify({"id": file_id }), 200
    return jsonify({"error":"Could not handle that request"}), 305


@app.route('/predict/<id>')
def predict_id(id):
    path = os.path.join(app.config['UPLOAD_FOLDER'], id)
    result = find_texts(path)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
