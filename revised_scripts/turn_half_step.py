#!/usr/bin/env python
import walk_init_biped as init
import turn_half_step_imp as turn_half
import back_walk as back
from sys_util import *
import sys

open_port()
set_baudrate()
# init.init_biped(portHandler)
turn_half.walk(portHandler, 1)
# back.walk(portHandler, int(sys.argv[1]))
close_port()

