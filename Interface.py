#!/usr/bin/env python
from tkinter import *
import matplotlib as plt
plt.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
  from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
  from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import rospy
from turtle_bot_1.srv import prenom, prenomResponse
from geometry_msgs.msg import Twist


#interface


global entrada
global direcc



root = Tk()
root.wm_title("Posicion del turtlebot")

frame = Frame(root)
frame.pack()

def servicioPrincipal():
    r = entrada.get()
    rospy.wait_for_service('turtle_bot_player')
    try:
        cliente_repr = rospy.ServiceProxy('turtle_bot_player', prenom)
        retorno = cliente_repr(r)
        print(retorno.nombre2)
    except rospy.ServiceException as e:
           print("Hubo un fallo inesperado: %s" %e )

def ventanaNombre():
    global entrada
    nom = Toplevel(root)
    nom.title("Documento a leer")
    nom.geometry("400x400")
    Label(nom, text = "Inserte el nombre").pack()
    entrada = Entry(nom)
    entrada.place(x=50,y=50)
    send = Button(nom, text="enviar", fg="blue", command = servicioPrincipal)
    send.pack(side = BOTTOM)
    nom.mainloop()

figure = Figure(figsize=(5, 5), dpi=100)
ax = figure.add_subplot(111)
ax.grid(visible=True)

def plot():
    x = np.random.rand(1, 10)
    y = np.random.rand(1, 10)
    ax.scatter(x, y)
    canvas.draw()
    plt.x

canvas = FigureCanvasTkAgg(figure, root)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)
canvas.get_tk_widget().pack()

datoY = Label(frame, text = 'Posicion en tiempo real', font = ("Arial",15), fg="blue")
datoY.pack( side = TOP )

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()

Boton = Button(frame, text = 'Reproducir', fg="red", command = ventanaNombre)
Boton.pack(side=BOTTOM)

def callback(data):
  global root
  global axes
  mainFrame = Frame(root)
  mainFrame.pack( side = BOTTOM )
  posx = data.linear.x
  posy = data.linear.y
  posz = data.angular.z
  ax.scatter(posx, posy)
  plt.xlim([0,2.5])
  plt.ylim([0,2.5])
  canvas.draw()

def interface():
  global root
  rospy.init_node('interface',anonymous=True)
  rospy.Subscriber("distancia", Twist, callback)
  root.mainloop()
  nom.mainloop()
  rospy.spin()


if __name__ == '__main__':
  interface()
