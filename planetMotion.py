import math
import threading
import tkinter as tk
from tkinter import Frame
from tkinter import Button
from tkinter import ttk
from tkinter import RIGHT
from tkinter import Canvas
from tkinter import LEFT

from datetime import datetime, timedelta

from body import Body
from controls import ControlPanel

pi = math.pi
G = 10

class MainWindow(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.timestep = 0.2
        self.drawTimestep = 1/1000
        
        self.pack()
        self.master.title("Main")
        self.controls = ControlPanel(self)
        self.controls.pack(side=RIGHT)
        self.can = Canvas(self, bg="grey", height=800, width=1200)
        self.can.pack(side=LEFT)
        self.bodies = [Body(), Body(), Body(), Body()]
        self.simThread = None
        self.resetOnCol = False

        self.setStartingPositions()
        self.drawBodies()

        self.controls.setTelemetry(self.bodies)
    
    def drawBody(self, b):
        r = b.radius
        x1 = b.posx - r
        x2 = b.posx + r
        y1 = b.posy - r
        y2 = b.posy + r
        
        b.oval = self.can.create_oval(x1, y1, x2, y2, fill=b.color)
    
    def drawBodies(self):
        for b in self.bodies:
            self.drawBody(b)

    def redrawBodies(self):
        for b in self.bodies:
            oval = b.oval
            self.can.move(oval, b.dx, b.dy)
            b.dx = b.dy = 0   

    def removeBodies(self):
        for b in self.bodies:
            self.can.delete(b.oval)
            b.oval = None

    def setStartingPositions(self):

        b = self.bodies[0]
        b.radius = 20
        b.posx = 500
        b.posy = 500
        b.velx = 3
        b.vely = -1
        b.mass = 300

        b = self.bodies[1]
        b.radius = 20
        b.posx = 300
        b.posy = 300
        b.velx = 2
        b.vely = 1
        b.color = "red"

        b = self.bodies[2]
        b.radius = 20
        b.posx = 400
        b.posy = 400
        b.velx = 2
        b.vely = 1
        b.color = "blue"

        b = self.bodies[3]
        b.radius = 20
        b.posx = 200
        b.posy = 500
        b.velx = 1
        b.vely = -2
        b.mass = 300
        b.color = "green"

    def resetBodies(self):
        self.setStartingPositions()
        self.removeBodies()
        self.can.delete('all')
        self.drawBodies()
        self.controls.updateTelemetry()
        
    def loadBodies(self):
        self.removeBodies()
        self.can.delete('all')
        self.bodies.clear()
        self.bodies = self.getBodiesFromFile("positions")
        self.drawBodies()
        self.controls.removeTelemetry()
        self.controls.setTelemetry(self.bodies)
    
    def getBodiesFromFile(self, fileName):
        bodies = []
        with open(fileName, 'r') as f:
            for line in f:
                params = line.replace("\n", "").split(" ")
                b = Body()
                b.loadParams(params)
                bodies.append(b)
        return bodies   

    def saveBodies(self, fileName):
        with open(fileName, 'w') as f:
            for b in self.bodies:
                f.write(b.getParamString() + "\n")

    def start(self):
        self.can.create_oval(200, 200, 100, 100)
    
    def calculateForcesOnBody(self, b, bodies):
        accx = 0
        accy = 0
        x = b.posx
        y = b.posy
        for otherBody in bodies:
            if otherBody != b:
                dx = (otherBody.posx - x)
                dy = (otherBody.posy - y)
                r = math.sqrt( (dx) ** 2 + (dy) ** 2 )
                acc = G * otherBody.mass / (r ** 2)
                
                if(dx != 0):
                    theta = abs(math.atan( (dy) / (dx) ))
                else:
                    theta = pi/2
                if(b.posx > otherBody.posx): #if right of
                    accx -= acc * math.cos(theta)
                else:
                    accx += acc * math.cos(theta)                  
                if(b.posy > otherBody.posy):  #if below                             
                    accy -= acc * math.sin(theta)
                else:
                    accy += acc * math.sin(theta)
        
        return (accx, accy)

    def next(self):
        ts = self.timestep
        for b in self.bodies:
            (accx, accy) = self.calculateForcesOnBody(b, self.bodies)

            b.velx += accx * ts
            b.vely += accy * ts
        
        for b in self.bodies:
            dx = b.velx * ts
            dy = b.vely * ts

            b.posx += dx
            b.dx += dx

            b.posy += dy
            b.dy += dy
        self.controls.updateTelemetry()

    def runCont(self):
        if(self.simThread == None):
            self.simThread = threading.Thread(target=self.runContThread)
            self.simThread.start()

    def stopCont(self):
        if(self.simThread != None):

            self.simThread.do_run = False
            self.simThread = None

    def runContThread(self):
        nextUpdate = datetime.now() + timedelta(0, self.drawTimestep)
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            self.next()
            if(nextUpdate < datetime.now()):
                self.redrawBodies()
                nextUpdate = datetime.now() + timedelta(0, self.drawTimestep)
                  
    def updateBody(self, b, newb):



        #update color
        b.color = newb.color
        self.can.itemconfig(b.oval, fill=b.color) 

        #update position
        dx = newb.posx - b.posx
        dy = newb.posy - b.posy
        self.can.move(b.oval, dx, dy)

        b.posx = newb.posx
        b.posy = newb.posy

        #update vel
        b.velx = newb.velx
        b.vely = newb.vely

        #update mass
        b.mass = newb.mass

        #update radius (must redraw)
        self.can.delete(b.oval)
        b.radius = newb.radius
        self.drawBody(b)

    def removeBody(self, b):
        self.bodies.remove(b)
        self.can.delete(b.oval)

    def updateResetOnCol(self, val):
        self.resetOnCol = val

    def test(self):
        for b in self.bodies:
            self.drawBody(b)



def main(): 
    MainWindow().mainloop()

if __name__ == '__main__':
    main()