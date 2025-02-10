import serial
import time

# Replace '/dev/ttyUSB0' with the correct port for your Arduino
def find_arduino_port():
    possible_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
    for port in possible_ports:
        try:
            ser = serial.Serial(port, 9600, timeout=1)
            ser.close()
            return port
        except (serial.SerialException, OSError):
            continue
    return None

arduino_port = find_arduino_port()
if arduino_port is None:
    print("Arduino not found. Check connections!")
    exit()

ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)  # Allow time for the connection to establish

try:
    while True:
        ser.write(b'Hello Arduino\n')  # Send data to Arduino
        time.sleep(1)
        
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            print("Received from Arduino:", response)
except KeyboardInterrupt:
    print("\nClosing serial connection.")
    ser.close()
