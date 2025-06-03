// Define pin numbers
const int stepPin = 5; 
const int dirPin = 2; 

const int stepsPerRevolution = 800; // Full steps per revolution
const int stepDelayMicroseconds = 400; // Speed control

void setup() {
  // Initialize Serial Communication
  Serial.begin(115200); // Match baud rate with Xavier

  // Set motor pins as outputs
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);

  // Ensure motor is off initially
  digitalWrite(stepPin, LOW);
}

void loop() {
  // Check if data is available from Xavier
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command
    Serial.print("Received command: ");
    Serial.println(command); // Echo the received command

    if (command == '1') {
      // Command 1: Turn left
      Serial.println("Turning left...");
      digitalWrite(dirPin, HIGH); // Set direction to left
      makeSteps(stepsPerRevolution); // Execute steps
    } 
    else if (command == '2') {
      // Command 2: Turn right
      Serial.println("Turning right...");
      digitalWrite(dirPin, LOW); // Set direction to right
      makeSteps(stepsPerRevolution); // Execute steps
    } 
    else {
      // Invalid command
      Serial.println("Invalid command received.");
    }
  }
}

// Function to make steps
void makeSteps(int steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicroseconds);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicroseconds);
  }
}
