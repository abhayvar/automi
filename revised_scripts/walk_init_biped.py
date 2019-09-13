#!/usr/bin/env python

# Author: Arunim Joarder

import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library


# Control table address
ADDR_MX_TORQUE_ENABLE        = [24,64]               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION        = [30,116]
ADDR_MX_PRESENT_POSITION     = [36,132]

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = [PacketHandler(1.0), PacketHandler(2.0)]

f = open("../revised_scripts/walk_angles.txt")
num_dxls = 0
for line in f:
    num_dxls += 1
f.close()

f = open("../revised_scripts/walk_angles.txt")
DXL_INFO_ALL = [0]*num_dxls
for dxl_id in range(num_dxls):
    DXL_INFO_ALL[dxl_id] = []
    line = f.readline()
    DXL_INFO_ALL[dxl_id].append([int(x) for x in line.split()])
f.close()

class Dxls:
    def __init__(self, ID, ProtocolVersion):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = 0
        self.ProtocolVersion = ProtocolVersion
DXL = []
for dxl_index in range(num_dxls):
    DXL.append(Dxls(DXL_INFO_ALL[dxl_index][0][0], DXL_INFO_ALL[dxl_index][0][1]))
    DXL[dxl_index].DXL_GOAL_POSITION_VALUE = DXL_INFO_ALL[dxl_index][0][2]

def init_biped(portHandler):
    for dxl_index in range(num_dxls):  
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler[DXL[dxl_index].ProtocolVersion - 1].write1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_TORQUE_ENABLE[DXL[dxl_index].ProtocolVersion - 1], TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler[DXL[dxl_index].ProtocolVersion - 1].getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler[DXL[dxl_index].ProtocolVersion - 1].getRxPacketError(dxl_error))
        # else:
        #     print("Dynamixel %d has been successfully connected" % (DXL[dxl_index].ID))

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler[DXL[dxl_index].ProtocolVersion - 1].write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_GOAL_POSITION[DXL[dxl_index].ProtocolVersion - 1], DXL[dxl_index].DXL_GOAL_POSITION_VALUE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler[DXL[dxl_index].ProtocolVersion - 1].getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler[DXL[dxl_index].ProtocolVersion - 1].getRxPacketError(dxl_error))