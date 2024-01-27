from PIL import Image
import os

def resize_images(source_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(source_folder, filename)
            img = Image.open(img_path)
            img_resized = img.resize((256, 256))
            img_resized.save(os.path.join(dest_folder, filename))

# Example usage
source_folder = 'Test'  # Replace with your source folder path
dest_folder = 'Test256'  # Replace with your destination folder path
resize_images(source_folder, dest_folder)
