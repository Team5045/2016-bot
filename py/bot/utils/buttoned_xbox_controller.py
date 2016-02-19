"""
buttoned_xbox_controller.py
===========================

The RobotPy `control.xbox_controller.XboxController` class does not
implement a "true" `GenericHID`, so we have to monkey-patch the controller
so we can still attach button handlers.
"""

from robotpy_ext.control.xbox_controller import XboxController


class ButtonedXboxController(XboxController):
    def getRawButton(self, button):
        # print('get raw button', button, self)
        # print(self.getLeftTrigger(), self.getRightTrigger(), self.getLeftBumper(), self.getRightBumper())
        if button == 'left_trigger':
            return self.getLeftTrigger()
        elif button == 'right_trigger':
            return self.getRightTrigger()
        elif button == 'left_bumper':
            # FIXME REVERSED THESE SINCE BUMPER BROKEN???
            return self.getRightBumper()
        elif button == 'right_bumper':
            return self.getLeftBumper()
        else:
            return self.ds.getStickButton(self.port, button)
