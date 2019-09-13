#!/usr/bin/env python
import rise_init_position
import sys_util as sys1
import sys_util_torso as sys2
import sys

if str(sys.argv[1]) == 't':
    sys2.open_port()
    sys2.set_baudrate()
    rise_init_position.init_biped(sys2.portHandler, str(sys.argv[1]), int(sys.argv[2]))
    sys2.close_port()
elif str(sys.argv[1]) == 'b':
    sys1.open_port()
    sys1.set_baudrate()
    rise_init_position.init_biped(sys1.portHandler, str(sys.argv[1]), int(sys.argv[2]))
    sys1.close_port()

