#!/usr/bin/env python
import turn_less_init
from sys_util import *
import sys

open_port()
set_baudrate()
turn_less_init.init_biped(portHandler, int(sys.argv[1]))
close_port()

