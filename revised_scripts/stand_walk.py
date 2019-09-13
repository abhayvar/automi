#!/usr/bin/env python
import walk_init_biped as init
import stand_to_walk as vel
import back_walk as back
from sys_util import *
import sys

open_port()
set_baudrate()
#init.init_biped(portHandler)
vel.walk(portHandler, int(sys.argv[1]))
close_port()

