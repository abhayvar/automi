#!/usr/bin/env python

# Author: Arunim Joarder
import os
import time
from dynamixel_sdk import *                    # Uses Dynamixel SDK library


# Control table address
ADDR_AX_TORQUE_ENABLE         = 24               # Control table address is different in Dynamixel model
ADDR_AX_GOAL_POSITION         = 30
ADDR_AX_PRESENT_POSITION      = 36
ADDR_AX_MOVING                = 46

LEN_AX_GOAL_POSITION          = 4
LEN_AX_TORQUE_ENABLE          = 1
LEN_AX_PRESENT_POSITION       = 4

# num_steps = int(sys.argv[1])
t_sub_steps = 0.001

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE                    = 57600              # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque



DXL_MOVING_STATUS_THRESHOLD = 10                # Dynamixel moving status threshold

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler1 = PacketHandler(1.0)


f = open("../revised_scripts/rise_angles_torso.txt")
num_dxls_torso = 0
for line in f:
    num_dxls_torso += 1
f.close()

f = open("../revised_scripts/rise_angles_torso.txt")
DXL_INFO_ALL_TORSO = [0]*num_dxls_torso
for dxl_index in range(num_dxls_torso):
    DXL_INFO_ALL_TORSO[dxl_index] = []
    line = f.readline()
    DXL_INFO_ALL_TORSO[dxl_index].append([int(x) for x in line.split()])
f.close()


class Dxls:
    def __init__(self, ID):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = [0]*0

    def profileVel(self, goal_index):
        return 1000,500


# Setup all Dynamixels        
DXL_TORSO = [0]*0
def setupDynamixelsTorso():
    for dxl_index in range(0, num_dxls_torso):
        DXL_TORSO.append(Dxls(DXL_INFO_ALL_TORSO[dxl_index][0][0]))
        for goal_index in range(0, len(DXL_INFO_ALL_TORSO[0][0]) - 1):
            DXL_TORSO[dxl_index].DXL_GOAL_POSITION_VALUE.append(DXL_INFO_ALL_TORSO[dxl_index][0][goal_index + 1])


# Enable Dynamixel Torque
def enableTorqueTorso(portHandler):
    for dxl_index in range(0, num_dxls_torso):
        dxl_comm_result, dxl_error = packetHandler1.write1ByteTxRx(portHandler, DXL_TORSO[dxl_index].ID, ADDR_AX_TORQUE_ENABLE, TORQUE_ENABLE)       
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler1.getTxRxResult(dxl_comm_result), DXL_TORSO[dxl_index].ID)
        elif dxl_error != 0:
            print("%s" % packetHandler1.getRxPacketError(dxl_error), DXL_TORSO[dxl_index].ID)
        # else:
        #     print("Dynamixel %d has been successfully connected" % (DXL_TORSO[dxl_index].ID))


# time.sleep(8)
def rise(portHandler):
    setupDynamixelsTorso()    
    
    enableTorqueTorso(portHandler)

    groupSyncWrite1 = GroupSyncWrite(portHandler, packetHandler1, ADDR_AX_GOAL_POSITION, LEN_AX_GOAL_POSITION)
      
    for goal_index in range(0, len(DXL_INFO_ALL_TORSO[0][0]) - 1):
                    
        # Write goal position
        # Add all Dynamixels' goal position value to groupSyncWrite1 parameter storage
        for dxl_index in range(num_dxls_torso):
                
            # Allocate goal position value into byte array
            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(DXL_TORSO[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_LOWORD(DXL_TORSO[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_LOBYTE(DXL_HIWORD(DXL_TORSO[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_HIWORD(DXL_TORSO[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index]))]
            dxl_addparam_result = groupSyncWrite1.addParam(DXL_TORSO[dxl_index].ID, param_goal_position)
            if dxl_addparam_result != 1:
                print("[ID:%03d] groupSyncWrite1 addparam failed" % (DXL_TORSO[dxl_index].ID))
                quit()  
        
        # SyncWrite goal position
        dxl_comm_result = groupSyncWrite1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler1.getTxRxResult(dxl_comm_result))

        # Clear SyncWrite parameter storage
        groupSyncWrite1.clearParam()
        time.sleep(0.5)
