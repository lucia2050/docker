import unittest
import os
from svm_service import predict_svm
from vgg19_service import predict_vgg

class TestPredictions(unittest.TestCase):
    def extract_label(self, filename):
        # Extract class label (e.g., 'disco' or 'pop') from the filename
        return os.path.splitext(filename)[0].split('.')[0]
    
    def test_svm_predictions(self):
        wav_files = ['pop.00003.wav']  # Add more files if necessary
        for wav_file in wav_files:
            prediction = predict_svm(f'/app/test_data/{wav_file}')
            label = self.extract_label(wav_file)
            self.assertIn(label,prediction)
           

    def test_vgg_predictions(self):
        wav_files = ['disco.00004.wav']  # Add more files if necessary
        for wav_file in wav_files:
            prediction = predict_vgg(f'/app/test_data/{wav_file}')
            label = self.extract_label(wav_file)
            self.assertIn(label,prediction)
           

if __name__ == '__main__':
    unittest.main()

     
   