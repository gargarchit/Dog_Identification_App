from flask import Flask, render_template, redirect, request, url_for
from inference import predict_breed_transfer
import os
import io
from PIL import Image

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def submit_data():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            image = file.read()
            predicted_breed = predict_breed_transfer(image_bytes = image)
            imag = Image.open(io.BytesIO(image))
            imag.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            result_dic = {
                'im' : file.filename,
                'breed' : predicted_breed
            }
            return render_template('index.html', dog=result_dic)
        return render_template("index.html")

if __name__ == '__main__':
    app.run()