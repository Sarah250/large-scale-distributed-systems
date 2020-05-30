class Msg():
    def __init__(self, vectorX):
        self.vectorX = vectorX
        self.type = "Init"

    def setType(self, value):
        self.final = value