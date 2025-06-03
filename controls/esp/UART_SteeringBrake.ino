#include <ESP32Servo.h>

// Pin Definitions
const int stepPin = 5;        // //orange Stepper motor step pin (GPIO 5)esp32
const int dirPin = 4;         ////yellow  Stepper motor direction pin (GPIO 4)esp32
const int servoPin = 13;      // Servo control pin (GPIO 13)
const int accelPin = 34;      // Analog input pin for acceleration (ADC1_CH0, GPIO 36)
//espRX--->XavierTX
//espTX--->XavierRX
///gndXAVIER14---> ALM(Green)
///gndXAVIER6---> ALM(Green)

                                             ///gndXAVIER14---> ALM(Green)


// Constants
const int stepsPerRevolution = 800; // Full steps per revolution for stepper motor
const int stepDelayMicroseconds = 400; // Delay between steps for speed control

// Objects
Servo brakeServo;             // Servo object for braking/acceleration control

// Variables
int accelValue = 0;           // Acceleration value (0-4095 from ESP32 ADC)
char command[3];              // Command array to store UART data (e.g., "01")

void setup() {
  // Initialize Serial Communication
  Serial.begin(115200);       // UART baud rate

  // Set motor pins as outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  // Initialize servo
  brakeServo.attach(servoPin);
  brakeServo.write(0);        // Start with the servo at 0 degrees (no brake)

  // Initialize stepper motor
  digitalWrite(stepPin, LOW);

  Serial.println("ESP32 System Initialized. Awaiting Commands...");
}

void loop() {
  // Check if UART data is available
  if (Serial.available() >= 2) { // Expecting 2-bit command (e.g., "01")
    Serial.readBytes(command, 2);  // Read 2 characters
    command[2] = '\0';            // Null-terminate the string for safety

    // Debugging - Print the received command
    Serial.print("Received command: ");
    Serial.println(command);

    // Parse the command
    int brakeCommand = command[0] - '0';  // Convert first bit to integer (brake)
    int steerCommand = command[1] - '0';  // Convert second bit to integer (steer)

    // Perform actions based on commands
    handleBrake(brakeCommand);
    handleSteering(steerCommand);

    // Optional: Read and process acceleration
    accelValue = analogRead(accelPin);  // Read acceleration value (0-4095 on ESP32 ADC)
    Serial.print("Acceleration value: ");
    Serial.println(accelValue);

    delay(100); // Small delay for stability
  }
}

// Function to handle braking using servo
void handleBrake(int brakeCommand) {
  if (brakeCommand == 1) {
    Serial.println("Braking...");
    brakeServo.write(180); // Apply brake (servo to 180 degrees)
  } else {
    Serial.println("Releasing brake...");
    brakeServo.write(0);   // Release brake (servo to 0 degrees)
  }
}

// Function to handle steering using stepper motor
void handleSteering(int steerCommand) {
  if (steerCommand == 1) {
    Serial.println("Steering left...");
    digitalWrite(dirPin, HIGH); // Set direction to left
    makeSteps(stepsPerRevolution);
  } else if (steerCommand == 0) {
    Serial.println("Steering right...");
    digitalWrite(dirPin, LOW);  // Set direction to right
    makeSteps(stepsPerRevolution);
  } else {
    Serial.println("Invalid steering command!");
  }
}

// Function to make steps with the stepper motor
void makeSteps(int steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicroseconds);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicroseconds);
  }
}
