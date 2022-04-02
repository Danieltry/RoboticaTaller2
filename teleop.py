#!/usr/bin/env python
import rospy
import os
from pynput import keyboard
from std_msgs.msg import String

#primer punto
#teleop

here= os.path.abspath(os.path.dirname(__file__))
parent = os.path.dirname(here)
print(parent+'/scripts')
k=None
pre = input('Guardar recorrido (conteste True o False)')
filepath = os.path.join(parent + '/scripts', 'pasos.txt')
#linSpeed = input('INGRESE SU VELOCIDAD LINEAL (0-70):')
#rotSpeed = input('INGRESE SU VELOCIDAD ANGULAR (0-180):')

def on_press(key):
  global k
  if key==keyboard.Key.esc:
    return False
  try:
    k = key.char
  except:
    k = key.name
  if k in ['s','w','a','d', 'b']:
    return False

def on_release(key):
  global k
  try:
    k = key.char
  except:
    k = key.name
  if k == 'w':
    k = 'W'
    return False
  elif k =='s':
    k='S'
    return False
  elif k == 'd':
    k = 'D'
    return False
  elif k=='a':
    k='A'
    return False

def instr(key):
 # global linSpeed
 # global rotSpeed
  global f
  global pre
  k = key
  if k in ['s','w','a','d' , 'W', 'S','A', 'D', 'b']:
    print(k)
    if k == 'w':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'w')
      return 'w'
    elif k == 's':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 's')
      return 's'
    elif k == 'a':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'a')
      return 'a'
    elif k == 'd':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'd')
        print(k)
      return 'd'
    elif k == 'W':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'W')
      return 'W'
    elif k == 'S':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'S')
      return 'S'
    elif k == 'D':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'D')
      return 'D'
    elif k == 'A':
      if pre == True:
        with open(filepath, 'a') as f:
          f.write( '\n' + 'A')
      return 'A'
    elif k == 'b':
        with open(filepath, 'a') as f:
          f.write( '\n' + 'b')
        exit()
        return 'b'

def comands():
  pub = rospy.Publisher('cmd_vel',String, queue_size=10) 
  rospy.init_node('teleop', anonymous=True)
  rate=rospy.Rate(10)
  msg=String()
  while not rospy.is_shutdown():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()
    instructionLinear = instr(k)
    if k in ['w','s','a','d', 'b']:
      msg = instructionLinear
    else:
      msg = 'b'
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
    
if __name__ == '__main__':

    comands()
