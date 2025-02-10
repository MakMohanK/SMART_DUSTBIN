import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
from tensorflow.keras.applications.efficientnet import preprocess_input # type: ignore

model_path = "./model/model_EfficientnetB0.h5"  
model = tf.keras.models.load_model(model_path)
class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']
im_shape = (224, 224)

image_dir = "./images" 
image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir)[:50]]

def preprocess_image(image_path):
    img = load_img(image_path, target_size=im_shape)
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Use EfficientNet preprocessing
    return img_array[0]  # Remove batch dimension


def perform_prediction():
    images = np.array([preprocess_image(img) for img in image_paths])

    # Perform predictions
    predictions = model.predict(images)

    data = []

    for i, pred in enumerate(predictions):
        predicted_class = np.argmax(pred)  # Get index of max confidence
        confidence_score = np.max(pred)  # Get highest confidence score
        # print(f"Image {i+1}: Predicted Class - {class_names[predicted_class]}, Confidence - {confidence_score:.4f}")
        data.append([predicted_class, confidence_score])

    # print(data)

    last_conf = 0
    last_index = 0
    for x in data:
        if x[1] > last_conf:
            last_index = x[0]
            last_conf = x[1]


    # Display results
    fig, axes = plt.subplots(5, 10, figsize=(20, 10))
    axes = axes.flatten()

    for i, img_path in enumerate(image_paths):
        img = load_img(img_path, target_size=im_shape)
        axes[i].imshow(img)
        axes[i].axis("off")
        axes[i].set_title(f"Pred: {np.argmax(predictions[i])}")
        axes[i].set_title("Pred: " + str(np.argmax(predictions[i])))


    plt.tight_layout()
    plt.show()
    # print("Confidence :", last_conf, "\t","Index:",last_index, "\t", class_names[last_index])
    return [last_conf, last_index, class_names[last_index]]


print(perform_prediction())




