#!/usr/bin/env python

# Author: Arunim Joarder

import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE         = 64               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION         = 116
ADDR_MX_PRESENT_POSITION      = 132
ADDR_MX_PROFILE_VELOCITY      = 112
ADDR_MX_PROFILE_ACCELERATION  = 108
ADDR_DRIVE_MODE               = 10

# num_steps = int(sys.argv[1])
t_sub_steps = 0.001

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE                    = 57600              # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque



DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold


# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

f = open("angles.txt")
num_dxls = 0
for line in f:
    num_dxls += 1
f.close()

DXL_PROFILE_ACCELERATION       =  5000
# print(DXL_PROFILE_ACCELERATION)

f = open("angles.txt")
DXL_INFO_ALL = [0]*num_dxls
for dxl_id in range(num_dxls):
    DXL_INFO_ALL[dxl_id] = []
    line = f.readline()
    DXL_INFO_ALL[dxl_id].append([int(x) for x in line.split()])
f.close()


class Dxls:
    def __init__(self, ID):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = [0]*0

    def profileVel(self, goal_index):
        profileVel = int((((abs((self.DXL_GOAL_POSITION_VALUE)[goal_index] - (self.DXL_GOAL_POSITION_VALUE)[goal_index+1])/4095.0)*60)/t_sub_steps)/0.229)
        # return profileVel
        return 30000
        

# time.sleep(8)
def walk(portHandler, num_steps):
    # Setup all Dynamixels
    DXL = [0]*0
    for dxl_index in range(0, num_dxls):
        DXL.append(Dxls(DXL_INFO_ALL[dxl_index][0][0]))
        for goal_index in range(0, len(DXL_INFO_ALL[0][0]) - 1):
            DXL[dxl_index].DXL_GOAL_POSITION_VALUE.append(DXL_INFO_ALL[dxl_index][0][goal_index + 1])
        
    for dxl_index in range(0, num_dxls):
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)       
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PROFILE_ACCELERATION, DXL_PROFILE_ACCELERATION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID)
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID)
        else:
            print("Dynamixel %d has been successfully connected" % (DXL[dxl_index].ID))

    for i in range(num_steps):
        for goal_index in range(len(DXL_INFO_ALL[0][0]) - 3, -1, -1):
        
            prof_vel = [0]*num_dxls
            for dxl_index in range(0, num_dxls):
                prof_vel[dxl_index] = DXL[dxl_index].profileVel(goal_index)
                print(DXL[dxl_index].profileVel(goal_index))
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PROFILE_VELOCITY, prof_vel[dxl_index])    
                if dxl_comm_result != COMM_SUCCESS:
                    print(packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID, 'vel')
                elif dxl_error != 0:
                    print(packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID, 'vel')
            
            
            # Write goal position
            for dxl_index in range(0, num_dxls):
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_GOAL_POSITION, DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])
               