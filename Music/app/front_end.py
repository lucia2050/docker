from flask import Flask, render_template, request
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename
import base64
import requests

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# URL des services SVM et VGG
svm_url = 'http://svm:5000/predict_svm'
vgg_url = 'http://vgg:5000/predict_vgg'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/templates/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

@app.route('/')
def index():
    return render_template('index.html', wav_data=None, svm_prediction=None, vgg_prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Envoyer le fichier WAV à SVM
        with open(file_path, 'rb') as wav_file:
            svm_response = requests.post(svm_url, files={'audio': wav_file})

        # Envoyer le fichier WAV à VGG
        with open(file_path, 'rb') as wav_file:
            vgg_response = requests.post(vgg_url, files={'audio': wav_file})

        # Lire et encoder le fichier .wav comme base64
        with open(file_path, 'rb') as wav_file:
            wav_data = base64.b64encode(wav_file.read()).decode('utf-8')

        # Récupérer les résultats des services SVM et VGG
        svm_prediction = svm_response.json()['prediction'] if svm_response.ok else 'Error predicting with SVM'
        vgg_prediction = vgg_response.json()['prediction'] if vgg_response.ok else 'Error predicting with VGG'

        return render_template('index.html', wav_data=wav_data, svm_prediction=svm_prediction, vgg_prediction=vgg_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
