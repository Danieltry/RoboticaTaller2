#include <ros.h>
#include <std_msgs/String.h>

#include <AFMotor.h>

String msg;
ros::NodeHandle node_handle;
std_msgs::String X;
//AF_DCMotor motor1(1);
//AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);


void subscriberCallback(const std_msgs::String& X) {
  msg = X.data;
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  if (msg == "w") {

    motor3.run(FORWARD);
    motor4.run(FORWARD);
  }
  else if (msg == "s") {

    motor3.run(BACKWARD);
    motor4.run(BACKWARD);
  }
  else if (msg == "d")
  {

    motor3.run(FORWARD);
    motor4.run(BACKWARD);
  }
  else if (msg == "a")
  {

    motor3.run(BACKWARD);
    motor4.run(FORWARD);
  }
  else if (msg == "b")
  {

    motor3.run(RELEASE);
    motor4.run(RELEASE);
  }
  

}

ros::Subscriber<std_msgs::String> cmd_vel("cmd_vel", &subscriberCallback);

void setup() {
  Serial.begin(57600);           // set up Serial library at 9600 bps
  Serial.println("Motor test!");

  // turn on motor
//  motor1.setSpeed(255);
//  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);



//  motor1.run(RELEASE);
//  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);

  node_handle.initNode();
  node_handle.subscribe(cmd_vel);
}

void loop() {


  node_handle.spinOnce();
  delay(100);
}
