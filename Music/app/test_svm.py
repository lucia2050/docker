import unittest
import os
from svm_service import predict_svm
import requests

svm_url = 'http://svm:5000/predict_svm'
class TestPredictions(unittest.TestCase):
    def extract_label(self, filename):
        # Extract class label (e.g., 'disco' or 'pop') from the filename
        return os.path.splitext(filename)[0].split('.')[0]
    
    def test_svm_predictions(self):
        wav_files = ['pop.00003.wav']  # Add more files if necessary
        for wav_file_f in wav_files:
            file_path= '/app/test_data/{wav_file_f}'
            with open(file_path, 'rb') as wav_file:
               svm_response = requests.post(svm_url, files={'audio': wav_file})
            svm_prediction = svm_response.json()['prediction'] if svm_response.ok else 'Error predicting with svm'
            label = self.extract_label(wav_file_f)
            self.assertIn(label,svm_prediction )

           

if __name__ == '__main__':
    unittest.main()

     
   
