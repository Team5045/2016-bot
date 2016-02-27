"""
config.py
=========

This file is used to store configuration variables for the robot. This is
benefial as it enables us to decouple logic from robot-specific variables,
like the port a particular motor is attached to.

General tip: In the heat of the competition you will probably find yourself
tweaking command/subsystem files themselves (e.g. "Oh nooo it's too fast wtf
slow it down hury hurry before the next match!!!"). This is to be expected, and
is FINE -- as long as you remember to go back after competition and clean up
all the code.
"""
import math

# Operator interface
OI_DRIVE_CONTROLLER = 0
OI_OPERATOR_CONTROLLER = 1
OI_INTAKE = 'right_trigger'
OI_OUTTAKE = 'left_trigger'
OI_SHOOT = 1  # "A" button
OI_JUST_SHOOT = 2  # "B" button
OI_AUTO_ALIGN = 3  # "X" button
OI_TOGGLE_INTAKE = 'right_bumper'
OI_TOGGLE_CAMERA = 'left_bumper'

# Drive train
DRIVE_FRONT_RIGHT_MOTOR = 1
DRIVE_FRONT_LEFT_MOTOR = 3
DRIVE_REAR_LEFT_MOTOR = 4
DRIVE_REAR_RIGHT_MOTOR = 2
DRIVE_MAX_SPEED = .75
DRIVE_SENSITIVITY = 0.4
DRIVE_RIGHT_ENCODER_A = 0
DRIVE_RIGHT_ENCODER_B = 1
DRIVE_LEFT_ENCODER_A = 2
DRIVE_LEFT_ENCODER_B = 3
DRIVE_ENCODER_DISTANCE_PER_PULSE = (math.pi * (10)) / 250  # Diameter (in) / ct

# Intake
INTAKE_MOTOR = 0
INTAKE_SOLENOID_FW = 0
INTAKE_SOLENOID_BW = 1
INTAKE_LOADED_LIMIT_SWITCH = 4

# Shooter
SHOOTER_MOTOR = 1

# Compressor
COMPRESSOR_DASHBOARD_KEY = 'editable--boolean--compressor'

# Misc
MISC_AUTO_COMMAND_DASHBOARD_KEY = 'editable--chooser--autonomous_command'
MISC_DRIVER_DIRECTION_DASHBOARD_KEY = 'editable--chooser--driver_direction'
