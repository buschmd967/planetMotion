class Body():
    def __init__(self):
        self.posx = 0
        self.posy = 0

        self.velx = 0
        self.vely = 0

        self.mass = 30
        self.radius = 1

        self.color = "yellow"

        #vars for canvas math
        self.oval = None
        self.dx = 0
        self.dy = 0

    def loadParams(self, params):
        self.color = params[0]
        self.posx = float(params[1])
        self.posy = float(params[2])
        self.velx = float(params[3])
        self.vely = float(params[4])
        self.mass = float(params[5])
        self.radius = float(params[6])
    
    def getParamString(self):
        return f"{self.color} {self.posx} {self.posy} {self.velx} {self.vely} {self.mass} {self.radius}"
