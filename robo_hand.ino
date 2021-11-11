// Robotic hand control using hand landmark detection
// Arduino controller interface code
// Fathi Mahdi Elsiddig
// 11/11/2021
// This code receives the data from main.py through serial communication

//#include <servo>
String x;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString();
 Serial.println(x);
 delay(500);
}
