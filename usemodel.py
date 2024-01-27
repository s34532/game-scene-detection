import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import numpy as np
import os

# Load the trained model
model = load_model('battle_model.keras')

# Directory containing images to predict
predict_directory = 'dataset\\testcombined'

# Function to preprocess the image
def preprocess_image(image_path, target_size=(256, 256)):
    image = load_img(image_path, target_size=target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0  # Normalization to match training
    return image

# Iterate over images in the directory
for filename in os.listdir(predict_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):  # Assuming JPG format
        file_path = os.path.join(predict_directory, filename)
        processed_image = preprocess_image(file_path)

        # Predicting the class
        prediction = model.predict(processed_image)
        if prediction[0][0] > 0.5:
            print(f"{filename}: Out of Battle")
        else:
            print(f"{filename}: In Battle")
