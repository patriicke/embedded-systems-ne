#include <SoftwareSerial.h>
SoftwareSerial configBt(10, 11);  // RX, TX

void setup() {
  Serial.begin(38400);
  configBt.begin(38400);
}

void loop() {
  if (configBt.available()) {
    Serial.print(configBt.readString());
  }
  if (Serial.available()) {
    configBt.write(Serial.read());
  }
}