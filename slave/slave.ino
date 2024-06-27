#include <SoftwareSerial.h>
SoftwareSerial bluetoothSerial(10, 11);

void setup() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);
}
void loop() {
  if (bluetoothSerial.available()) {
    Serial.print(bluetoothSerial.readString().c_str());
  }
  if (Serial.available()) {
    String serialData = Serial.readString();
    bluetoothSerial.write(serialData.c_str());
  }
}