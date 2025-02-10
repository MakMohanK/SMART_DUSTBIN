import os
import cv2
import time
import serial
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
from tensorflow.keras.applications.efficientnet import preprocess_input # type: ignore

print("[INFO]...INITIALIZED DEVICE")

image_dir = "./images" 
arduino_port = "/dev/ttyACM0"
model_path = "./model/model_EfficientnetB0.h5"  

ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)  # Allow time for the connection to establish

class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir)[:50]]

cap = cv2.VideoCapture(2)

im_shape = (224, 224)
MOTION_THR = 1500
WAIT_BEFORE = 10
MOTION_DETECTED = False
model = tf.keras.models.load_model(model_path)
ret, frame1 = cap.read()
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame1 = cv2.GaussianBlur(frame1, (21, 21), 0)


from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3") 

    

def classify_waste(item: str) -> str:
    waste_categories = {
        "o": {"biological", "paper"},
        "r": {"brown-glass", "green-glass", "metal", "white-glass", "cardboard", "clothes", "shoes", "trash", "battery", "plastic"}
    }
    
    for category, items in waste_categories.items():
        if item.lower() in items:
            return category
    return "x"

def preprocess_image(image_path):
    img = load_img(image_path, target_size=im_shape)
    img_array = img_to_array(img)  
    img_array = np.expand_dims(img_array, axis=0) 
    img_array = preprocess_input(img_array)  
    return img_array[0]  


def perform_prediction():
    data = []
    print("[INFO]...STARTED PREDICTION")
    images = np.array([preprocess_image(img) for img in image_paths])

    predictions = model.predict(images)

    for i, pred in enumerate(predictions):
        predicted_class = np.argmax(pred)  
        confidence_score = np.max(pred)  
        data.append([predicted_class, confidence_score])

    last_index, last_conf = max(data, key=lambda x: x[1], default=(0, 0))
    print("Confidence :", last_conf, "\t","Index:",last_index, "\t", class_names[last_index])
    return [last_conf, last_index, class_names[last_index]]

def capture_images():
    time.sleep(2)
    print("[INFO]...STARTED IMAGE CAPTURING")
    for i in range(50):  # Start capturing from 10th image to 50th image
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        if not ret:
            print("[ERROR]...CHECK CAMERA CONNECTION")
            break
        brightness_factor = 0.8 + (i / 100)  # Vary brightness from 0.8x to 1.0x
        bright_frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)
        image_path = os.path.join(image_dir, f"image_{i+1}.jpg")
        cv2.imwrite(image_path, bright_frame)
        cv2.imshow("Motion Detection", frame)
        if cv2.waitKey(20) & 0xFF == ord('q'): # press q to break code excecution
            break
        # time.sleep(0.3)
    print("[INFO]...END OF IMAGE CAPTURING")
    

text = "Welcome ! to smart dustbin system, I am happy to help you with sorting organic waste."
text_to_speech(text)

while True:
    ret, frame2 = cap.read()
    if not ret:
        print("[ERROR]...CHECK CAMERA CONNECTION")
        break
    
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    diff = cv2.absdiff(frame1, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, ans = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not MOTION_DETECTED:
        for contour in contours:
            if cv2.contourArea(contour) > MOTION_THR:  # Ignore small movements
                MOTION_DETECTED = True
    else:
        MOTION_DETECTED = False

    if (MOTION_DETECTED):
        MOTION_DETECTED = False
        text = "Trash detected let me think what type of waste it is."
        text_to_speech(text)
        print("[INFO]...MOTION DETECTED")
        for x in range(WAIT_BEFORE):
            ret, frame2 = cap.read()
            time.sleep(1) 
            print("[USER INFO]...WAIT FOR ", WAIT_BEFORE-x, " SECONDS")
            text = "wait for "+str(WAIT_BEFORE-x)+" seconds"
            text_to_speech(text)
        capture_images()

        conf, ind, clss = perform_prediction()

        if conf > 0.50:
            data_to_uno = classify_waste(clss)
            if data_to_uno == 'o':
                text = "As per my knowwledge, it is considered as organic waste hence driping it to organic bin."
                text_to_speech(text)
            elif data_to_uno == 'r':
                text = "As per my knowwledge, it is considered as recycle or disposable type of waste hence droping it in other bin."
                text_to_speech(text)
            ser.write(f"{data_to_uno}\n".encode())  
            time.sleep(1)
        else:
            data_to_uno = "x"
            ser.write(f"{data_to_uno}\n".encode())  
            time.sleep(1)

        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(response)
                if "Closing" in response:
                    print("[INFO]...DONE WITH OPRATION")
                    time.sleep(8) # wait for 5 sec to bin fully close
                    break
        
        for _ in range(5):  # Adjust this number based on latency
            cap.read()
        
    cv2.imshow("Motion Detection", frame2)

    frame1 = gray
    
    if cv2.waitKey(20) & 0xFF == ord('q'): # press q to break code excecution
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
