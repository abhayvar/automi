#!/usr/bin/env python
import rise_biped as rise

from sys_util import *
# import sys

open_port()
set_baudrate()
rise.rise(portHandler)
close_port()

