#!/usr/bin/env python
import RPi.GPIO as GPIO
import rospy
import time
import threading
import numpy as np
from std_msgs.msg import UInt16MultiArray
from geometry_msgs.msg import Twist


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.IN)

stateLast1 = GPIO.input(17)
stateLast2 = GPIO.input(27)
rotationCount1 = 0
rotationCount2 = 0
stateCount1 = 0
stateCountTotal1 = 0
stateCount2 = 0
stateCountTotal2 = 0

#encoders

circ = 201 #mm
statesPerRotation = 4
distancePerStep = circ/statesPerRotation

def calculoDeTiempo(stateCount, stateCountTotal, pin):
  global statesPerRotation
  while stateCount <= statesPerRotation:
    stateCurrent = GPIO.input(pin)
    stateLast = GPIO.input(pin)
    if stateLast != stateCurrent:
        stateCountTotal+=1
        stateCount+=1
    elif stateCount == statesPerRotation:
        stateCount = 0
        end_time = time.time()
    stateLast = stateCurrent
  return end_time, stateCount, stateCountTotal


def pasos():
  global stateCount1
  global stateCountTotal1
  global stateCount2
  global stateCountTotal2
  start_time = time.time()
  #Agregar coment1 aca

  #Agregar comment2 aca    
  
  t1 = threading.Thread(target = calculoDeTiempo, args = (stateCount1, stateCountTotal1, 17,)) 
  t2 = threading.Thread(target = calculoDeTiempo, args = (stateCount2, stateCountTotal2, 27,))
  
  t1.start()
  t2.start()
  
  t1.join()
  t2.join()
  
  duracion1 = t1[0] - start_time
  duracion2 = t2[0] - start_time
    
  distance1 = distancePerStep*stateCountTotal1    
  distance2 = distancePerStep*stateCountTotal2
  velocidad1 = distance1/duracion1
  velocidad1 = distance2/duracion2
  print(stateCount2)
  print(stateCountTotal2)
  print(distance)
  return [distance1,distance2,0], [velocidad1, velocidad2] 

def calcularPosicion(arreglo):
  x = [0]
  y = [0]
  theta = [np.pi/6]
  rw = 3.2
  l = 17.6
  
  Vr = arreglo[0]/rw
  Vl = arreglo[1]/rw
  dt = 0.1
  for i in np.arange(0,3,dt):
    x.append(x[-1]+0.5*(Vr+Vl)*np.cos(theta[-1])*dt)
    y.append(x[-1]+0.5*(Vr+Vl)*np.cos(theta[-1])*dt)
    theta.append(theta[-1] + 1*(Vr-Vl)*dt)
  return [x,y,theta]
  
  

def comandos():
  pub = rospy.Publisher('distancia',Twist, queue_size=10) 
  rospy.init_node('encoders', anonymous=True)
  rate=rospy.Rate(10)
  msg=Twist()
  while not rospy.is_shutdown():
    
    total = calcularPosicion(pasos()[1])
    msg.linear.x = total[0]
    msg.linear.y = total[1]
    msg.linear.z = total[2] 
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
    

if __name__ == '__main__':

    comandos()
    
    #Borradores:
    #Comment 1
    #  while stateCount1 < statesPerRotation:
#    stateCurrent1 = GPIO.input(17)
#   stateLast1 = GPIO.input(17)
#    if stateLast1 != stateCurrent1:
#        stateCountTotal1+=1
#        stateCount1+=1
#    stateLast1 = stateCurrent1
#    if stateCount1 == statesPerRotation:
#        stateCount1 = 0
#        end_time1 = time.time()
#        duracion1 = end_time - start_time
   #comment2
#  while stateCount2 < statesPerRotation:
#      stateCurrent2 = GPIO.input(27)
#      stateLast2 = GPIO.input(27)
#    if stateLast2 != stateCurrent2:
#        stateCountTotal2+=1   
#        stateCount2+=1
#    stateLast1 = stateCurrent1
#    if stateCount2 == statesPerRotation:
#        stateCount2 = 0
#        end_time2 = time.time()
