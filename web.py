from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import Required
from werkzeug.utils import secure_filename
import os	

# TODO: couldn't make bootstrap work

UPLOAD_FOLDER = "./public/uploads/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
# just a random string
app.config['SECRET_KEY'] = 'y8fwpI0IABFV1P8ovbmN'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('public/js', path)
    
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('public/css', path)
    

@app.route('/')
def get_home():
    return render_template('index.html')
    
@app.route('/', methods=['POST'])
def home():

    # 1. load the template for homepage containing - done
    # 2. form for file upload and submit/predict button - done
    # 3. upload the file and save in the (-database)/file - done
    # 4. redirect to the predict page 
    # 5. use POST method to take the file - done

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))                               
    return redirect("/")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
