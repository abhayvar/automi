#!/usr/bin/env python
import init_position
from sys_util import *
import sys

open_port()
set_baudrate()
init_position.init_biped(portHandler, int(sys.argv[1]))
close_port()

