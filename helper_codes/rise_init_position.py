
#!/usr/bin/env python

# Author: Arunim Joarder

import os
import sys
import time
from dynamixel_sdk import *                    # Uses Dynamixel SDK library


# Control table address
ADDR_MX_TORQUE_ENABLE        = [24,64]               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION        = [30,116]
ADDR_MX_PRESENT_POSITION     = [36,132]

LEN_MX_PRESENT_POSITION      = 4
LEN_MX_GOAL_POSITION         = 4

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = [PacketHandler(1.0), PacketHandler(2.0)]

f = open("rise_init9pos.txt")
num_dxls = 0
for line in f:
    num_dxls += 1
f.close()

f_torso = open("rise_init9pos_torso.txt")
num_dxls_torso = 0
for line in f_torso:
    num_dxls_torso += 1
f_torso.close()

f = open("rise_init9pos.txt")
DXL_INFO_ALL = [0]*num_dxls
for dxl_id in range(num_dxls):
    DXL_INFO_ALL[dxl_id] = []
    line = f.readline()
    DXL_INFO_ALL[dxl_id].append([int(x) for x in line.split()])
f.close()

f_torso = open("rise_init9pos_torso.txt")
DXL_INFO_ALL_TORSO = [0]*num_dxls_torso
for dxl_id in range(num_dxls_torso):
    DXL_INFO_ALL_TORSO[dxl_id] = []
    line = f_torso.readline()
    DXL_INFO_ALL_TORSO[dxl_id].append([int(x) for x in line.split()])
f_torso.close()

DATA = [DXL_INFO_ALL_TORSO, DXL_INFO_ALL]
NUM_DXLS = [num_dxls_torso, num_dxls]

class Dxls:
    def __init__(self, ID, ProtocolVersion):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = 0
        self.ProtocolVersion = ProtocolVersion

DXL = []


def init_biped(portHandler, part, pos):

    if part == 'b':
        t = 1
    elif part == 't':
        t = 0
    else:
        print('choose b/w part: b (biped) or t (torso) ?')

    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler[t], ADDR_MX_GOAL_POSITION[t], LEN_MX_GOAL_POSITION)

    for dxl_index in range(NUM_DXLS[t]):
        DXL.append(Dxls(DATA[t][dxl_index][0][0], DATA[t][dxl_index][0][1]))
        DXL[dxl_index].DXL_GOAL_POSITION_VALUE = DATA[t][dxl_index][0][pos + 1]

    for dxl_index in range(NUM_DXLS[t]):  
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler[t].write1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_TORQUE_ENABLE[t], TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler[t].getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler[t].getRxPacketError(dxl_error))
        else:
            print('', end = '')
            # print("Dynamixel %d has been successfully connected" % (DXL[dxl_index].ID))

        
        # Allocate goal position value into byte array
        param_goal_position = [DXL_LOBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE)), DXL_HIBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE)), DXL_LOBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE)), DXL_HIBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE))]
        dxl_addparam_result = groupSyncWrite.addParam(DXL[dxl_index].ID, param_goal_position)
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncWrite addparam failed" % (DXL[dxl_index].ID))
            quit() 

    # SyncWrite goal position
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    # Clear SyncWrite parameter storage
    groupSyncWrite.clearParam()
    # print('---------------------------------', goal_index, '---------------------------------')
