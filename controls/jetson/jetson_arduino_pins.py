import serial
import time

# Open the serial port (adjust '/dev/ttyTHS1' to your UART device on the Jetson)
arduino = serial.Serial('/dev/ttyTHS1', 115200, timeout=1)

def read_from_arduino():
    while True:
        # Read data from the Arduino
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()  # Read and decode the data
            print("Received from Arduino:", data)
        time.sleep(0.1)

if __name__ == '__main__':
    print("Starting communication with Arduino...")
    read_from_arduino()

