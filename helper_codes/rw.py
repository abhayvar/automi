#!/usr/bin/env python

# Author: Madhur Deep Jain

import os
import sys

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = [64, 24]             # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = [116, 30]
ADDR_MX_PRESENT_POSITION   = [132, 36]

# Default setting
#DXL_ID                      = int(sys.argv[1])                 # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
#DXL_GOAL_POSITION_VALUE     = int(sys.argv[2])           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)
num_dxls = [[1,2,9,11,12,13,14,15,16,17],[1,2,3,5,6,7,18]]
# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = [PacketHandler(2.0), PacketHandler(1.0)]

# Open port

# Read present position
def read_position(portHandler, protocol_version):
	for DXL_ID in num_dxls[protocol_version]:
		dxl_present_position, dxl_comm_result, dxl_error = packetHandler[protocol_version].read4ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION[protocol_version])
		if dxl_comm_result != COMM_SUCCESS:
		    print("%s" % packetHandler[protocol_version].getTxRxResult(dxl_comm_result))
		elif dxl_error != 0:
		    print("%s" % packetHandler[protocol_version].getRxPacketError(dxl_error))

		print("[ID:%03d] PresPos:%03d" % (DXL_ID, dxl_present_position))

    # if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
