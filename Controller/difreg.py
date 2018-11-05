


class difreg():
    """docstring for difreg."""
    int = 0
    ki = 0.75
    ti = 0.1
    kp = 1
    def regulate(self, leftsensor, rightsensor):
        err = leftsensor - rightsensor
        self.int = self.int + abs(err)
        self.clamp()
        if abs(err) > 5:
            if leftsensor < rightsensor:
                return self.kp*err*-1+self.int*self.ki*self.ti,0
            else:
                return 0,self.kp*err+self.int*self.ki*self.ti
        self.int = 0
        return 0,0
    def clamp(self):
        if self.int > 1000:
            self.int = 1000
        if self.int < 0:
            self.int = 0
