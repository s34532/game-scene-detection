import time
import mss.tools
import mss
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from shared_state import battle_status, status_lock
model = load_model('battle_model.keras')



updateFrequency = 5

def preprocess_image(sct_img):
    
    image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    # Now you can resize, convert to array, etc.
    image = image.resize((256, 256))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0  
    return image

def update_battle_status():
    sct = mss.mss()
    monitor = sct.monitors[3]

    while True:
        # grab image from monitor
        sct_img = sct.grab(monitor)
        # preprocess image from monitor
        processed_image = preprocess_image(sct_img)

        # Predicting the class
        prediction = model.predict(processed_image, verbose = 0)
        
        with status_lock:
            if prediction[0][0] > 0.5:
                battle_status['in_battle'] = True
                print("Out of Battle")

            else:
                battle_status['in_battle'] = False
                print("In Battle")


        time.sleep(updateFrequency)

def main():
    
    update_battle_status()




if __name__ == "__main__":
    main()