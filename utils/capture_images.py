import cv2
import numpy as np
import os

# Create a directory to store images
save_dir = "./images"
os.makedirs(save_dir, exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
else:
    print("Opening Camera")

# Capture 50 images with different brightness levels
for i in range(50):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image.")
        break
    
    # Apply brightness adjustment
    brightness_factor = 0.8 + (i / 100)  # Vary brightness from 0.8x to 1.0x
    bright_frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)
    
    # Save image
    image_path = os.path.join(save_dir, f"image_{i+1}.jpg")
    cv2.imwrite(image_path, bright_frame)
    
    cv2.imshow("Captured Image", bright_frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print(f"Captured 50 images in '{save_dir}' with varying brightness levels.")
