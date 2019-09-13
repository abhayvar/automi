#!/usr/bin/env python
import turn_right_less_imp as vel
from sys_util import *
import sys

open_port()
set_baudrate()
vel.turn(portHandler)
close_port()

