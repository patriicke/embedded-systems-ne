#include <SoftwareSerial.h>
#include <LiquidCrystal_I2C.h>

SoftwareSerial bluetoothSerial(10, 11);
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int buzzer = 9;

void initComponents() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);

  pinMode(buzzer, OUTPUT);

  lcd.init();
  lcd.backlight();
}

void operateBuzzer(String customerName, String itemCount) {
  lcd.clear();
  lcd.setCursor(0, 0);

  lcd.print(customerName);
  lcd.setCursor(0, 1);
  lcd.print("Items: " + itemCount);

  tone(buzzer, 1000);
  delay(1000);
  noTone(buzzer);
  delay(1500);

  lcd.clear();
}

void parseBluetoothData(String bluetoothData) {
  String customerName = "";
  String itemCount = "";

  int customerIndex = bluetoothData.indexOf("Customer: ");
  if (customerIndex != -1) {
    int customerEndIndex = bluetoothData.indexOf("\n", customerIndex);
    if (customerEndIndex != -1) {
      customerName = bluetoothData.substring(customerIndex + 10, customerEndIndex);
    }
  }

  int itemsIndex = bluetoothData.indexOf("\nCart Items:\n");
  if (itemsIndex != -1) {
    int itemsEndIndex = bluetoothData.indexOf("\n", itemsIndex + 13);
    if (itemsEndIndex == -1) {
      itemsEndIndex = bluetoothData.length();
    }
    itemCount = bluetoothData.substring(itemsIndex + 13, itemsEndIndex);
  }

  operateBuzzer(customerName, itemCount);
}

void setup() {
  initComponents();
}

void loop() {
  if (bluetoothSerial.available()) {
    String bluetoothData = bluetoothSerial.readString();
    parseBluetoothData(bluetoothData);
  }
  if (Serial.available()) {
    String serialData = Serial.readString();
    bluetoothSerial.write(serialData.c_str());
  }
}
