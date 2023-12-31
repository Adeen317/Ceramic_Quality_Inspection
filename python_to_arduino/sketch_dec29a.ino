const int ledPin = 12;  // Define the pin connected to the LED

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command
    if (command == 'D' ) {
      digitalWrite(ledPin, HIGH); // Turn on the LED if 'D' is received // Keep the LED on for 1 second // Turn off the LED
    }
    if(command == 'B'){
      digitalWrite(ledPin, LOW);
    }
    }
    // You can add more conditions for other commands if needed
}
