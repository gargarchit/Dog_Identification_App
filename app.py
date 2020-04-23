from flask import Flask, render_template, redirect, request
from inference import predict_breed_transfer

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def submit_data():
    if request.method == 'POST':
        file = request.files['file']
        image = file.read()
        predicted_breed = predict_breed_transfer(image_bytes = image)
    return render_template('index.html', dog=predicted_breed)


if __name__ == '__main__':
    app.run()