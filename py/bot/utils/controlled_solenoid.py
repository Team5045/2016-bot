import wpilib


class ControlledSolenoid(object):
    def __init__(self, fw_port, bw_port):
        self.solenoid = wpilib.DoubleSolenoid(fw_port, bw_port)
        self.state = self.solenoid.get()

    def set(self, state):
        if state != self.state:
            self.state = state
            self.solenoid.set(self.state)

    def get(self):
        return self.state

    def toggle(self):
        if self.state == wpilib.DoubleSolenoid.Value.kForward:
            self.set(wpilib.DoubleSolenoid.Value.kReverse)
        else:
            self.set(wpilib.DoubleSolenoid.Value.kForward)

    def deploy(self):
        self.set(wpilib.DoubleSolenoid.Value.kForward)

    def retract(self):
        self.set(wpilib.DoubleSolenoid.Value.kReverse)
