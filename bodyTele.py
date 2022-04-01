import tkinter as tk
from tkinter import Frame
from tkinter import Button

from body import Body


class BodyTelemetry( Frame ):
    def __init__(self, b, parent):
        super().__init__(parent)
        self.grid()
        self.b = b
        self.parent = parent

        self.initStringVars()
        self.initLabels()
        self.initEntries()
        self.initButtons()

        self.drawLabels()
        self.drawButtons()

    def initStringVars(self):
        self.colorVar = tk.StringVar(self, f"{self.b.color}")
        self.posxVar = tk.StringVar(self, f"{self.b.posx:.2f}")
        self.posyVar = tk.StringVar(self, f"{self.b.posy:.2f}")
        self.velxVar = tk.StringVar(self, f"{self.b.velx:.2f}")
        self.velyVar = tk.StringVar(self, f"{self.b.vely:.2f}")
        self.massVar = tk.StringVar(self, f"{self.b.mass}")
        self.radiusVar = tk.StringVar(self, f"{self.b.radius}")

    def initEntries(self):
        self.colorEnt = tk.Entry(self, textvariable=self.colorVar, width=7, justify='center')
        self.posxEnt = tk.Entry(self, textvariable=self.posxVar, width=6)
        self.posyEnt = tk.Entry(self, textvariable=self.posyVar, width=6)
        self.velxEnt = tk.Entry(self, textvariable=self.velxVar, width=6)
        self.velyEnt = tk.Entry(self, textvariable=self.velyVar, width=6)
        self.massEnt = tk.Entry(self, textvariable=self.massVar, width=6)
        self.radiusEnt = tk.Entry(self, textvariable=self.radiusVar, width=6)

    def initLabels(self):
        self.colorLab = tk.Label(self, text="Color: ")
        self.posxLab = tk.Label(self, text="X: ")
        self.posyLab = tk.Label(self, text="Y: ")
        self.velxLab = tk.Label(self, text="vX: ")
        self.velyLab = tk.Label(self, text="vY: ")
        self.massLab = tk.Label(self, text="m: ")
        self.radiusLab = tk.Label(self, text="r: ")


    def initButtons(self):
        self.updateButton = Button(self, text="Update", command=self.updateBody)
        self.removeButton = Button(self, text="Remove", command=self.remove)

    def setSep(self, sep):
        self.sep = sep

    def remove(self):
        self.parent.parent.removeBody(self.b)
        self.sep.destroy()
        self.destroy()

    def update(self):
        self.colorVar.set(f"{self.b.color}")
        self.posxVar.set(f"{self.b.posx:.2f}")
        self.posyVar.set(f"{self.b.posy:.2f}")
        self.velxVar.set(f"{self.b.velx:.2f}")
        self.velyVar.set(f"{self.b.vely:.2f}")
    
    def updateBody(self):
        newb = Body()
        newb.color = self.colorEnt.get()
        newb.posx = float(self.posxEnt.get())
        newb.posy = float(self.posyEnt.get())
        newb.velx = float(self.velxEnt.get())
        newb.vely = float(self.velyEnt.get())
        newb.mass = float(self.massEnt.get())
        newb.radius = float(self.radiusEnt.get())

        self.parent.parent.updateBody(self.b, newb)
        self.update()


    def drawLabels(self):
        self.colorLab.grid(column=1, row=0)
        self.colorEnt.grid(column=2, row=0)

        self.posxLab.grid(column=0, row=1)
        self.posxEnt.grid(column=1, row=1)
        self.posyLab.grid(column=2, row=1)
        self.posyEnt.grid(column=3, row=1, padx = (10, 10))

        self.velxLab.grid(column=0, row=2)
        self.velxEnt.grid(column=1, row=2)
        self.velyLab.grid(column=2, row=2)
        self.velyEnt.grid(column=3, row=2)

        self.massLab.grid(column=0, row=3)
        self.massEnt.grid(column=1, row=3)
        self.radiusLab.grid(column=2, row=3)
        self.radiusEnt.grid(column=3, row=3)
        
    def drawButtons(self):
        self.removeButton.grid(column=2, row=10)
        self.updateButton.grid(column=2, row=11)