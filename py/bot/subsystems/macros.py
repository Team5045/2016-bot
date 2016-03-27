import csv
import json
import glob
import os

from wpilib.command import Subsystem
from wpilib.timer import Timer

from bot import config


MACRO_FILE_FORMAT = '/home/lvuser/macros/{}'


class Macros(Subsystem):

    # Subsystems for which to record state
    SUBSYTEM_NAMES = ['drive_train', 'intake', 'shooter']

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.mark_recording(False)
        self.mark_playing(False)

    def get_time(self):
        return Timer.getFPGATimestamp()

    def get_state(self):
        return {
            name: getattr(self.robot, name).get_state()
            for name in self.SUBSYTEM_NAMES
        }

    def restore_state(self, state):
        for name in self.SUBSYTEM_NAMES:
            if name in state:
                getattr(self.robot, name).restore_state(state[name])

    def make_macro_writer(self, name):
        return MacroWriter(name)

    def make_macro_reader(self, name):
        return MacroReader(name)

    def get_recorded_macros(self):
        return sorted([os.path.basename(p) for p in
                       glob.glob(MACRO_FILE_FORMAT.format('*'))], reverse=True)

    def mark_recording(self, recording):
        self.robot.jetson.put_value(config.OI_MACRO_RECORD, recording,
                                    valueType='boolean')

    def mark_playing(self, playing):
        self.robot.jetson.put_value(config.OI_MACRO_PLAY, playing,
                                    valueType='boolean')


class MacroWriter(object):

    def __init__(self, name):
        self.f = open(MACRO_FILE_FORMAT.format(name), 'w')
        self.writer = csv.DictWriter(
            self.f, fieldnames=['time'] + Macros.SUBSYTEM_NAMES)
        self.writer.writeheader()

    def write(self, time, state):
        row = {'time': time}

        for name in Macros.SUBSYTEM_NAMES:
            row[name] = json.dumps(state[name])

        self.writer.writerow(row)

    def end(self):
        self.f.close()


class MacroReader(object):

    def __init__(self, name):
        self.f = open(MACRO_FILE_FORMAT.format(name), 'r')
        self.reader = csv.DictReader(self.f)

    def items(self):
        for line in self.reader:
            time = float(line.pop('time'))
            state = {k: json.loads(v) for k, v in line.items()}
            yield time, state

    def end(self):
        self.f.close()
