#!/bin/bash
# setup.sh: One‐time setup script to install dependencies

echo "Installing Python dependencies..."
pip install kivy>=2.1.0 kivymd>=1.1.1 tflite-runtime>=2.9.0 requests>=2.28.0 pillow>=9.0.0 numpy>=1.21.0 plyer>=2.0.0

echo "Setup complete. Make sure to place 'model.tflite' and 'labels.txt' into 'foodsnap_app/app/assets/'."
