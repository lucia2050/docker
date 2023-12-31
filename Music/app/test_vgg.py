import unittest
import os
from svm_service import predict_svm
from vgg19_service import predict_vgg
import requests
vgg_url = 'http://vgg:5000/predict_vgg'

class TestPredictions(unittest.TestCase):
    def extract_label(self, filename):
        # Extract class label (e.g., 'disco' or 'pop') from the filename
        return os.path.splitext(filename)[0].split('.')[0]

    def test_vgg_predictions(self):
        wav_files = ['disco.00004.wav']  # Add more files if necessary
        for wav_file_f in wav_files:
            file_path = f'/app/test_data/{wav_file_f}'
            with open(file_path, 'rb') as wav_file:
                vgg_response = requests.post(vgg_url, files={'audio': wav_file})
            vgg_prediction = vgg_response.json()['prediction'] if vgg_response.ok else 'Error predicting with VGG'
            label = self.extract_label(wav_file_f)
            self.assertIn(label, vgg_prediction)
           

if __name__ == '__main__':
    unittest.main()

     
   
