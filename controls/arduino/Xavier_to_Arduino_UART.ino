#include <SPI.h>

void setup() {
  Serial.begin(115200); // Match baud rate
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    char receivedChar = Serial.read(); // Read one character at a time
    Serial.print("Received: ");
    Serial.println(receivedChar); // Echo the character back
  }

  // Send data continuously while listening
  Serial.println("Sending: Hello from Arduino!"); // Send data
  delay(1000); // Adjust this delay based on your needs
}
