///////////////////////////////////////////////////////////////////////////

// Robotic hand control using hand landmark detection
// Arduino controller interface code
// Fathi Mahdi Elsiddig
// 11/11/2021
// This code receives the data from main.py through serial communication

/////////////////////////////////////////////////////////////////////////////

#include <Servo.h>

////////////////////////////////////////////////////////////////////////

Servo servo_wrist;
Servo servo_pinky;
Servo servo_m_f;
Servo servo_r_f;
Servo servo_i_f;

const int wrist = 3;
const int pinky = 5;
const int middle_finger = 6;
const int ring_finger = 10;
const int index_finger = 9;
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
 Serial.begin(2000000,SERIAL_8N1);
 Serial.setTimeout(0.8);
 pinMode(wrist,OUTPUT);
 pinMode(pinky,OUTPUT);
 pinMode(middle_finger,OUTPUT);
 pinMode(ring_finger,OUTPUT);
 pinMode(index_finger, OUTPUT);
 servo_wrist.attach(wrist);
 servo_pinky.attach(pinky);
 servo_m_f.attach(middle_finger);
 servo_r_f.attach(ring_finger);
 servo_i_f.attach(index_finger);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////

void loop()
{

 while (!Serial.available());
 data = Serial.readString();
 //Serial.println(data);
 wrist_angle = atof(data.c_str())*100;
 pinky_angle = atof(data.c_str()+6)*100;
 m_f_angle = atof(data.c_str()+12)*100;
 r_f_angle = atof(data.c_str()+18)*100;
 i_f_angle = atof(data.c_str()+24)*100;
 //if (i_f_angle > 70.0)
 //{
   //i_f_angle = 70.0;
 //}
 
 //else if (i_f_angle < 40.0)
 //{
   //i_f_angle = 40.0;
 //}
 //Serial.print("value before: ");
 //Serial.println(i_f_angle);// for debugging only
 //Serial.println(data);
 //Serial.println(wrist_angle);// for debugging only
 //Serial.println(pinky_angle);// for debugging only
 //Serial.println(m_f_angle);// for debugging only
 //Serial.println(r_f_angle);// for debugging only
 wrist_angle = map(wrist_angle,50,60,180,50);
 m_f_angle = map(m_f_angle,40,70,170,0);
 r_f_angle = map(r_f_angle,40,70,170,0);
 i_f_angle = map(i_f_angle,40,70,170,0);
 pinky_angle = map(pinky_angle,40,70,170,0);
 Serial.print("value after: ");
 //Serial.println(i_f_angle);// for debugging only
 //analogWrite(wrist,wrist_angle);
 //analogWrite(pinky,pinky_angle);
 //analogWrite(middle_finger,m_f_angle);
 //analogWrite(ring_finger,r_f_angle);
 //analogWrite(index_finger,i_f_angle);
 servo_i_f.write(i_f_angle);
 servo_m_f.write(m_f_angle);
 servo_r_f.write(r_f_angle);
 servo_pinky.write(pinky_angle);
 servo_wrist.write(wrist_angle);
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
