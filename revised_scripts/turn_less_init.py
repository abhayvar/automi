
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
ADDR_MX_MOVING               = 122

LEN_MX_PRESENT_POSITION      = 4
LEN_MX_GOAL_POSITION         = 4

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(2.0)

f = open("turning_10degree.txt")
num_dxls = 0
for line in f:
    num_dxls += 1
f.close()

f = open("turning_10degree.txt")
DXL_INFO_ALL = [0]*num_dxls
for dxl_id in range(num_dxls):
    DXL_INFO_ALL[dxl_id] = []
    line = f.readline()
    DXL_INFO_ALL[dxl_id].append([int(x) for x in line.split()])
f.close()

f = open("../revised_scripts/walk_angles.txt")
DXL_INFO_ALL_1 = [0]*num_dxls
for dxl_id in range(num_dxls):
    DXL_INFO_ALL_1[dxl_id] = []
    line = f.readline()
    DXL_INFO_ALL_1[dxl_id].append([int(x) for x in line.split()])
f.close()

class Dxls:
    def __init__(self, ID, ProtocolVersion):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = 0
        self.ProtocolVersion = ProtocolVersion

DXL = []

def isMoving(portHandler):
    value = 1
    for dxl_index in range(num_dxls):
        moving_status, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_MOVING)
        if moving_status:
            value = 0

    return value

def init_biped(portHandler, pos):

    for dxl_index in range(num_dxls):
        DXL.append(Dxls(DXL_INFO_ALL[dxl_index][0][0], DXL_INFO_ALL[dxl_index][0][1]))
        DXL[dxl_index].DXL_GOAL_POSITION_VALUE = DXL_INFO_ALL[dxl_index][0][pos + 1]

    for dxl_index in range(num_dxls):  
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_TORQUE_ENABLE[DXL[dxl_index].ProtocolVersion - 1], TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print('', end = '')
            # print("Dynamixel %d has been successfully connected" % (DXL[dxl_index].ID))

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_GOAL_POSITION[DXL[dxl_index].ProtocolVersion - 1], DXL[dxl_index].DXL_GOAL_POSITION_VALUE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

    time.sleep(0.2)
    for dxl_index in range(num_dxls):
        present_pos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PRESENT_POSITION[1])
        error = DXL_INFO_ALL_1[dxl_index][0][pos] - present_pos

        print("%.2d : %d" %(DXL[dxl_index].ID, error))
    print()

    # Initialize GroupSyncRead instace for Present Position
    groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_MX_PRESENT_POSITION[1], LEN_MX_PRESENT_POSITION)

    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)

    for dxl_index in range(num_dxls):
        dxl_addparam_result = groupSyncRead.addParam(DXL[dxl_index].ID)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % DXL[dxl_index].ID)
            quit()

    while 1:
        if isMoving(portHandler):
            # print('fo')
            break
        
    goal_pos = [0]*num_dxls
    flag_groupSyncRead = 1
    flag_groupSyncWrite2 = 0
    i = 1
    while flag_groupSyncRead:
        # print('fo1')
        flag_groupSyncRead = 0

        # Syncread present position
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupsyncread data of Dynamixels is available
        for dxl_index in range(num_dxls):
            dxl_getdata_result = groupSyncRead.isAvailable(DXL[dxl_index].ID, ADDR_MX_PRESENT_POSITION[1], LEN_MX_PRESENT_POSITION)
            if dxl_getdata_result != True:
                print("[ID:%03d] groupSyncRead getdata failed" % DXL[dxl_index].ID)
                quit()

        # Get Dynamixels present position value
        for dxl_index in range(num_dxls):
            dxl_present_position = groupSyncRead.getData(DXL[dxl_index].ID, ADDR_MX_PRESENT_POSITION[1], LEN_MX_PRESENT_POSITION)
            goal_pos[dxl_index] = DXL[dxl_index].DXL_GOAL_POSITION_VALUE

            error = DXL[dxl_index].DXL_GOAL_POSITION_VALUE - dxl_present_position

            if abs(error) > DXL_MOVING_STATUS_THRESHOLD:
                flag_groupSyncRead = 1
                flag_groupSyncWrite2 = 1
                goal_pos[dxl_index] = DXL[dxl_index].DXL_GOAL_POSITION_VALUE + i*error

                param_goal_position1 = [DXL_LOBYTE(DXL_LOWORD(goal_pos[dxl_index])), DXL_HIBYTE(DXL_LOWORD(goal_pos[dxl_index])), DXL_LOBYTE(DXL_HIWORD(goal_pos[dxl_index])), DXL_HIBYTE(DXL_HIWORD(goal_pos[dxl_index]))]
            
                dxl_addparam_result = groupSyncWrite.addParam(DXL[dxl_index].ID, param_goal_position1)
                if dxl_addparam_result != 1:
                    print("[ID:%03d] groupSyncWrite addparam failed" % (DXL[dxl_index].ID))
                    quit()

        if flag_groupSyncWrite2:
            dxl_comm_result = groupSyncWrite.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

            groupSyncWrite.clearParam()

        if not flag_groupSyncRead:
            for dxl_index in range(num_dxls):
                print('ID: %0.3d ' %DXL[dxl_index].ID, goal_pos[dxl_index])

        i += 1