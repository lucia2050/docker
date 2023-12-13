from flask import Flask, request, jsonify
import joblib
import librosa
import numpy as np
import sklearn
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

app = Flask(__name__)

# Charger le modèle SVM
model_filename = '/app/models/svm_model.joblib'
loaded_classifier = joblib.load(open(model_filename, 'rb'))

# Fonction d'extraction des caractéristiques
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)

def zero_cross(x):
    n0 = 9000
    n1 = 9100
    zero_crossings = librosa.zero_crossings(x[n0:n1], pad=False)
    return sum(zero_crossings)

def spec_center(x, sr):
    spectral_centroids = normalize(librosa.feature.spectral_centroid(y=x, sr=sr)[0])
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames)
    ma = max(spectral_centroids)
    return t[np.where(spectral_centroids == ma)[0][0]]

@app.route('/predict_svm', methods=['POST'])
def predict_svm():
    try:
        # Assurez-vous que 'audio' est la clé correcte dans la requête multipart
        file = request.files['audio']
        x, sr = librosa.load(file, sr=None)  # Chargez le fichier WAV

        # ... Traitement des caractéristiques audio ...

        # Faire la prédiction
        new_example_features = np.array([[zero_cross(x), round(spec_center(x, sr), 2)]])
        prediction = loaded_classifier.predict(new_example_features)

        # Retourner le résultat
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
