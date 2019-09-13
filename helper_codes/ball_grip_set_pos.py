#!/usr/bin/env python
import ball_grip_init
import sys_util_torso as sys2
import sys

sys2.open_port()
sys2.set_baudrate()
ball_grip_init.grip(sys2.portHandler)
sys2.close_port()


