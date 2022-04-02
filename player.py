#!/usr/bin/env python
import rospy
import os
from std_msgs.msg import String
from turtle_bot_1.srv import prenom, prenomResponse

#player

global lin
global rot
#lin = 70
#rot = 180



def recorrerDeNuevo(directorio):
    archivo = open(directorio, 'r')
    lineas = archivo.readlines()
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate=rospy.Rate(10)
    msg=Twist()
    for k in lineas:
        if k in ['s\n','w\n','a\n','d\n' , 'pausa']:
          print(k)
          if k == 'w\n':
              msg = 'w'
              rospy.loginfo(msg)
              pub.publish(msg)
              rate.sleep()
          elif k == 's\n':
              msg = 's'
              rospy.loginfo(msg)
              pub.publish(msg)
              rate.sleep()
          elif k == 'a\n':
              msg = 'a'
              rospy.loginfo(msg)
              pub.publish(msg)
              rate.sleep()
          elif k == 'd\n':
              msg = 'd'
              rospy.loginfo(msg)
              pub.publish(msg)
              rate.sleep()
          elif k == 'pausa':
              msg = 'b'
              rospy.loginfo(msg)
              pub.publish(msg)
              rate.sleep()
              exit()
        # linea = lineas.readline()


#Ending

def handle(req):
    nombr = '/home/danielros/catkin_ws/src/turtle_bot_1/scripts/%s' % req.nombre1
    #Added for 4th
    recorrerDeNuevo(nombr)
    #Ending
    return prenomResponse(nombre2 = nombr)

def Servicio():
    rospy.Service('turtle_bot_player', prenom, handle)

def main():
    Servicio()
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('turtlebot_cmdVel', anonymous = False)
    main()
