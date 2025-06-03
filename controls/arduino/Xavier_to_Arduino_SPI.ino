#include <SPI.h>
#include <Servo.h>

#define BRAKING 0xFF
#define RELEASE 0x11
#define SERVO 9

Servo brakes;
int pos = 0;
bool flag = false;
bytes rx;

// currently the module only implements emergency breaks
// if required we can implement a slowed down brake as well

void setup(){
    pinMode(CS, INPUT_PULLUP); // ensuring that initially SS is 1 (disabled)
    pinMode(SCK, INPUT);
    pinMode(COPI, INPUT);
    pinMode(CIPO, OUTPUT);

    bitClear(SPCR, MSTR); // clearing Master bit to make controller act like slave 
    bitSet(SPCR, SPE); // enabling SPI Port
    SPI.attachInterrupt(); // ISR for SPI

    Serial.begin(115_200); // for debugging purposes
    // Initializing the servo motor
    brakes.attach(SERVO);
}

void ISR(SPI_STC_vect){
    flag = true;
}

void loop(){
    if (flag){
        rx = SPDR;
        brakes(rx);
        SPDR = 0x00; // emptying the SPDR register
        flag = false;
    }
}

void brakes(byte state){
    if (state == BRAKING){
        brakes.write(180)
        Serial.println("Braking");
    }
    else if (state == RELEASE){
       brakes.write(0);
       Serial.println("Releasing Brakes");
    }
}
