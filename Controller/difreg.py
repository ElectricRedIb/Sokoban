class difreg():
    """docstring for difreg."""
    int = 0
    kp = 2.5
    ki = 20
    ti = 0.01
    kd = 2.5
    td = ti
    lastErr = 0
    def regulate(self, leftsensor, rightsensor):
        err = leftsensor - rightsensor
        self.int = self.int + err
        self.dif = abs(self.lastErr - err)
        self.lastErr = err
        self.clamp()

        #if abs(err) > 5:
        if leftsensor < rightsensor:
            return self.kp*err*-1+abs(self.int)*self.ki*self.ti*self.dif*self.kd*self.td,0
        else:
            return 0,self.kp*err+abs(self.int)*self.ki*self.ti*self.dif*self.kd*self.td
        #self.int = 0
        #return 0,0
    def clamp(self):
        if self.int > 50000:
            self.int = 50000
        if self.int < -50000:
            self.int = -50000
    def reset(self):
        self.err = 0
        self.int = 0
        self.dif = 0
        self.lastErr = 0
