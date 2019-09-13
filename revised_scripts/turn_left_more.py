#!/usr/bin/env python
import walk_init_biped as init
import turn_left_more_imp as vel
import back_walk as back
from sys_util import *
import sys

open_port()
set_baudrate()
# init.init_biped(portHandler)
vel.walk(portHandler, 1)
# back.walk(portHandler, int(sys.argv[1]))
close_port()

