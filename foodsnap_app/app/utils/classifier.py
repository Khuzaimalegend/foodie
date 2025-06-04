import os
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

class FoodClassifier:
    def __init__(self, model_path: str, labels_path: str):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        with open(labels_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

    def preprocess(self, img_path: str):
        img = Image.open(img_path).convert('RGB').resize((224, 224))
        input_data = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
        return input_data

    def predict(self, img_path: str, top_k: int = 3):
        input_data = self.preprocess(img_path)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        top_indices = output_data.argsort()[-top_k:][::-1]
        results = [(self.labels[i], float(output_data[i])) for i in top_indices]
        return results
