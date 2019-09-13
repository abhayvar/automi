#!/usr/bin/env python
import rise_torso as rise

from sys_util_torso import *
# import sys

open_port()
set_baudrate()
rise.rise(portHandler)
close_port()

