WHITE = 2

class lineFollow():
    """docstring for lineFollow."""
    speed = 0
    setpoint = 80
    kp = 1
    ki = 1
    int = 0
    err = 0
    def __init__(self, speed, rawsensor):
        self.speed = speed
        self.setpoint = rawsensor
        print(rawsensor)
    def clamp(self):
        if self.int > 50:
            self.int = 50
        if self.int < 0:
            self.int = 0
    def clampOut(self,input):
        if input > self.speed:
            return self.speed
        if input < 0:
            return 0
        return input
    def regPID(self,rawsensor):
        self.err = self.setpoint - rawsensor
        self.int = self.int + self.err
        self.clamp()
        if rawsensor > 70:
            self.int  = 0
        return self.clampOut(self.err * self.kp + self.int * self.ki)
    def newsetpoint(self,rawsensor):
        self.setpoint = rawsensor
    def reset(self):
        self.err = 0
        self.int = 0
