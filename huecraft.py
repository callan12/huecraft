from tkinter import *
from qhue import Bridge
from PIL import ImageGrab
import time
from threading import Timer,Thread,Event

class LightController():
	def __init__(self, interval, parent):
		self.interval = interval
		self.parent = parent
		print("Coords: {0}".format(self.parent.coords[0]))

		self.coords = (self.parent.coords[0][0],self.parent.coords[0][1])######TEMP

		self.thread = Timer(self.interval,self.repeat)
		self.b = Bridge('192.168.1.<Your bridge IP here>','Yourusernamehere') #Placeholder for public username until I implement that feature
		self.lights = self.b.lights

	def repeat(self):
		img = ImageGrab.grab(bbox=(0,0,2560,1440)) #x1, y1, x2, y2
		color = img.getpixel(self.coords)
		print(color)
		self.setLightColor(color)

		self.thread = Timer(self.interval,self.repeat)
		self.thread.start()

	def start(self):
		self.thread.start()

	def cancel(self):
		self.thread.cancel()

	def setLightColor(self, rgb):
		red = rgb[0]/255
		green = rgb[1]/255
		blue = rgb[2]/255

		x = (0.5767309*red + 0.1855540*green + 0.1881852*blue)
		y = (0.2973769*red + 0.6273491*green + 0.0752741*blue)
		z = (0.0270343*red + 0.0706872*green + 0.9911085*blue)

		x = x/(x+y+z)
		y = y/(x+y+z)

		self.b.lights(1, 'state', xy=[x,y])

class Overlay:
	def __init__(self, master):
		#window creation
		self.master = master

		#config
		self.master.config(cursor="target")
		self.master.attributes('-alpha', 0.3)
		self.master.attributes("-fullscreen", True)

		#class variables
		self.coords = [[],[],[]]
		self.index = 0

		#bindings
		self.master.bind('<Escape>', self.close)
		self.master.bind('<Button 1>', self.clickCoord)
		self.master.bind('<Key>', self.key)

	def close(self, event):
		controller = LightController(0.5, self)
		controller.start()
		self.master.withdraw()

	def clickCoord(self, event):
		coord = [event.x, event.y]
		self.coords[self.index] = coord
		print(self.coords[0])

	def key(self, event):
		if event.char in ('1','2','3'):
			self.index = int(event.char)-1
			print(self.index)

	def recover(self):
		self.master.deiconify()

class Main:
	def __init__(self, master):
		self.master = master
		self.master.geometry('300x500')

		#Buttons
		self.overlayBtn = Button(master, text='Overlay', command=self.overlay)
		self.overlayBtn.pack()

	def overlay(self):
		overlay = Overlay(root)

root = Tk()
main = Main(root)
root.mainloop()

