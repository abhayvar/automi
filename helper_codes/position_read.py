#!/usr/bin/env python
from sys_util_torso import *
import sys
import rw

open_port()
set_baudrate()
if int(sys.argv[1]) == 1:
    rw.read_position(portHandler, 1)
elif int(sys.argv[1]) == 2:
    rw.read_position(portHandler, 0)
close_port()


