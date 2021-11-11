///////////////////////////////////////////////////////////////////////////

// Robotic hand control using hand landmark detection
// Arduino controller interface code
// Fathi Mahdi Elsiddig
// 11/11/2021
// This code receives the data from main.py through serial communication

/////////////////////////////////////////////////////////////////////////////

//#include <Servo.h>

////////////////////////////////////////////////////////////////////////

//Servo servo_wrist;
//Servo servo_pinky;
//Servo servo_m_f;
//Servo servo_r_f;
//Servo servo_i_f;

const int wrist = 3;
const int pinky = 5;
const int middle_finger = 6;
const int ring_finger = 9;
const int index_finger = 10;
float wrist_angle = 0;
float pinky_angle = 0;
float m_f_angle = 0;
float r_f_angle = 0;
float i_f_angle = 0;
//String msg[5];
//String *Ptr;
String  data;
////////////////////////////////////////////////////////////////////////////////////////////////

void setup()
{
 Serial.begin(115200);
 Serial.setTimeout(0.8);
 pinMode(wrist,OUTPUT);
 pinMode(pinky,OUTPUT);
 pinMode(middle_finger,OUTPUT);
 pinMode(ring_finger,OUTPUT);
 pinMode(index_finger,OUTPUT);
 //servo_wrist.attach(wrist);
 //servo_pinky.attach(pinky);
 //servo_m_f.attach(middle_finger);
 //servo_r_f.attach(ring_finger);
 //servo_i_f.attach(index_finger);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////

void loop()
{

 while (!Serial.available());
 data = Serial.readString();
 wrist_angle = atof(data.c_str());
 Serial.println(data); // for debugging only
 delay(10);
 //Ptr = data;
 //wrist_angle = atof(data);	
 //pinky_angle = atof(+2data);
 //m_f_angle = atof(+2data);
 //r_f_angle = atof(+2data);
 //i_f_angle = atof(+2data);
 //Serial.println(wrist_angle);
 //Serial.println(pinky_angle);
 //Serial.println(m_f_angle);
 //Serial.println(r_f_angle);
 //Serial.println(i_f_angle);
 
} 
