import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from tkinter import IntVar
from tkinter import Button
from tkinter import Checkbutton



from bodyTele import BodyTelemetry


class ControlPanel(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        self.parent = parent

        tk.Label(self, text="Controls").grid(column=0, row=0)   
        # ttk.Label(self, text="Reset on Collision").grid(column 0, row 5)

        self.initVars()
        self.initButtons()
        self.telemetryLabels = []
        self.telemetrySeparators = []

    def initVars(self):
        self.resetOnCol = IntVar()

    def initButtons(self):
        self.runContButton = Button(self, text="Run", command=self.runCont)
        self.runContButton.grid(column=0, row=1)
        parent = self.parent
        Button(self, text="Step", command=parent.next).grid(column=0, row=2)
        # Button(self, text="Reset", command=parent.resetBodies).grid(column=0, row=3)
        Button(self, text="Save", command=self.saveBodies).grid(column=0, row=4)
        Button(self, text="Load", command=parent.loadBodies).grid(column=0, row=5)
        Button(self, text="Remove Telem", command=self.removeTelemetry).grid(column=0, row=9)

        #Check Boxes
        Checkbutton(self, text="Reset On Collision", variable=self.resetOnCol, onvalue=1, offvalue=0, command=self.updateResetOnCol).grid(column=0, row=8)
        
    def saveBodies(self):
        self.parent.saveBodies("positions")

    def updateResetOnCol(self):
        self.parent.updateResetOnCol(self.resetOnCol.get() == 1)

    def runCont(self):
        text = self.runContButton['text']
        if(text == "Run"):
            self.parent.runCont()
            self.runContButton['text'] = "Stop"
        elif(text == "Stop"):
            self.parent.stopCont()
            self.runContButton['text'] = "Run"
    
    def setTelemetry(self, bodies):
        
        for b in bodies:
            self.telemetryLabels.append(BodyTelemetry(b, self))
        for i in range(len(self.telemetryLabels)):
            sep = ttk.Separator(self, orient='horizontal')
            self.telemetrySeparators.append(sep)
            sep.grid(column=0, row=10+(i*2), sticky="ew", pady=(10, 10))
            self.telemetryLabels[i].setSep(sep)
            self.telemetryLabels[i].grid(column=0, row=10+(i*2 + 1))

    def removeTelemetry(self):
        for bT in self.telemetryLabels:
            bT.destroy()
        self.telemetryLabels.clear()
        for sep in self.telemetrySeparators:
            sep.destroy()
        self.telemetrySeparators.clear()

    def updateTelemetry(self):
        for bT in self.telemetryLabels:
            bT.update()