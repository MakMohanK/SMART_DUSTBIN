import asyncio
from gpiozero import Button
import cv2
import numpy as np
from picamera2 import Picamera2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from time import sleep
from signal import pause
import serial

import serial.tools.list_ports

# GPIO Setup
button = Button(4, pull_up=True, bounce_time=0.1)


def get_available_ports():
    """Lists all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Get the list of available ports
available_ports = get_available_ports()

if not available_ports:
    print("No serial ports found! Please connect a device and try again.")
    exit()

print("Available serial ports:")
for i, port in enumerate(available_ports):
    print(f"{i + 1}: {port}")

# Automatically select the first port or let the user choose
selected_port = available_ports[0]


# Set up the serial connection
ser = serial.Serial(
    port=selected_port,         # Replace 'COM3' with your port name (e.g., '/dev/ttyUSB0' on Linux)
    baudrate=9600,       # Match the baud rate of your device
    timeout=1            # Read timeout in seconds
)

# Check if the serial connection is open
if ser.is_open:
    print(f"Connected to {ser.port} at {ser.baudrate} baud rate.")
    ser.write(f"90\n".encode())


# Load the trained model
model = load_model('model_checkpoint.keras')

# Initialize the Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
sleep(2)  # Allow the camera to warm up

codeRunning = False

# Function to set the servo angle asynchronously
async def setAngle(angle):
    try:
        ser.write(f"{angle}\n".encode())
        await asyncio.sleep(2)
        ser.write(f"90\n".encode())
    except:
        print('ARDUINO PORT DISCONNECTED')
        pass;

# Function to predict the class of a single image
async def predict_single_image(img_array):
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)
    if prediction[0] > 0.5:
        return "Class R"
    else:
        return "Class O"

# Function to capture and process the camera feed
async def cam_start():
    global codeRunning
    print("Started process")
    frame = picam2.capture_array()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    resized_frame = cv2.resize(frame_rgb, (150, 150))
    img_array = image.img_to_array(resized_frame)

    predicted_class = await predict_single_image(img_array)
    print(f"The predicted class is: {predicted_class}")

    if predicted_class == "Class R":
        await setAngle(40)
    elif predicted_class == "Class O":
        await setAngle(130)

    #cv2.putText(frame_rgb, f"Prediction: {predicted_class}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    #cv2.imshow("Video Feed", frame_rgb)
    codeRunning = False
    print("Process finished")

# Function to handle button press and start processing
async def start_processing():
    global codeRunning
    print("Button pressed")
    if not codeRunning:
        codeRunning = True
        await cam_start()

# Wrapper for button press handling
def handle_button_press():
    asyncio.run(start_processing())

# Attach button press event
button.when_pressed = handle_button_press

# Start the asyncio event loop
try:
    pause()  # Keep the script running
except KeyboardInterrupt:
    ser.close() 
    print("Program stopped by user")
