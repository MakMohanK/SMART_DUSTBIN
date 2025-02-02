import os
import numpy as np
import tensorflow as tf
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

# Load the trained model
model_path = "./model/model_EfficientnetB0.h5"  # Update with the correct model path
model = tf.keras.models.load_model(model_path)

class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

print(model.summary())  # Check the model architecture  


# Image shape
im_shape = (224, 224)

# Directory containing images (Update with the correct path)
image_dir = "./images"  # Update with the correct folder containing images
image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir)[:50]]

# Load and preprocess images
# def preprocess_image(image_path):
#     img = load_img(image_path, target_size=im_shape)
#     # img_array = img_to_array(img) / 255.0  # Normalize
#     img_array = (img_to_array(img) - 127.5) / 127.5  # Normalize to -1 to 1  
#     return img_array

def preprocess_image(image_path):
    img = load_img(image_path, target_size=im_shape)
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Use EfficientNet preprocessing
    return img_array[0]  # Remove batch dimension

# Prepare batch of images
images = np.array([preprocess_image(img) for img in image_paths])

# Perform predictions
predictions = model.predict(images)

for i, pred in enumerate(predictions):
    predicted_class = np.argmax(pred)  # Get index of max confidence
    confidence_score = np.max(pred)  # Get highest confidence score
    print(f"Image {i+1}: Predicted Class - {class_names[predicted_class]}, Confidence - {confidence_score:.4f}")


# Display results
fig, axes = plt.subplots(5, 10, figsize=(20, 10))
axes = axes.flatten()

for i, img_path in enumerate(image_paths):
    img = load_img(img_path, target_size=im_shape)
    axes[i].imshow(img)
    axes[i].axis("off")
    # axes[i].set_title(f"Pred: {np.argmax(predictions[i])}")
    axes[i].set_title("Pred: " + str(np.argmax(predictions[i])))


plt.tight_layout()
plt.show()

# Print confidence values
# for i, pred in enumerate(predictions):
#     print(f"Image {i+1}: Confidence Values - {pred}")
