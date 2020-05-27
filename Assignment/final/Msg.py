class Msg():
    def __init__(self, vectorX):
        self.vectorX = vectorX
        self.final = False

    def setFinal(self):
        self.final = True