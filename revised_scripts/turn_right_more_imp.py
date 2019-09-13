#!/usr/bin/env python

# Author: Arunim Joarder
import matplotlib.pyplot as plt
import os
import time
from dynamixel_sdk import *                    # Uses Dynamixel SDK library


# Control table address
ADDR_MX_TORQUE_ENABLE         = 64               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION         = 116
ADDR_MX_PRESENT_POSITION      = 132
ADDR_MX_PROFILE_VELOCITY      = 112
ADDR_MX_PROFILE_ACCELERATION  = 108
ADDR_MX_DRIVE_MODE            = 10
ADDR_MX_MOVING                = 122
ADDR_MX_P_GAIN_POSITION       = 84

LEN_MX_GOAL_POSITION          = 4
LEN_MX_PROFILE_VELOCITY       = 4
LEN_MX_PROFILE_ACCELERATION   = 4
LEN_MX_TORQUE_ENABLE          = 1
LEN_MX_PRESENT_POSITION       = 4

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



DXL_MOVING_STATUS_THRESHOLD = 10                # Dynamixel moving status threshold

PROFILE_VELOCITY            = 2
PROFILE_ACCELERATION        = 1

PI = 3.14159

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)


f = open("../revised_scripts/walk_angles.txt")
num_dxls = 0
for line in f:
    num_dxls += 1
f.close()

f = open("../revised_scripts/walk_angles.txt")
DXL_INFO_ALL = [0]*num_dxls
for dxl_index in range(num_dxls):
    DXL_INFO_ALL[dxl_index] = []
    line = f.readline()
    DXL_INFO_ALL[dxl_index].append([int(x) for x in line.split()])
f.close()

# print(len(DXL_INFO_ALL[0][0]))

class Dxls:
    def __init__(self, ID):
        self.ID = ID
        self.DXL_GOAL_POSITION_VALUE = [0]*0

    def profileVel(self):
        total_time = 900
        accel_time = 450

        # pos_diff = abs(self.DXL_GOAL_POSITION_VALUE[goal_index] - self.DXL_GOAL_POSITION_VALUE[goal_index - 1])/ 4096
        
        # max_velocity = (2 * pos_diff * 1000 * 60 / float(total_time + accel_time)) / (0.229)

        # acceleration = (max_velocity * 1000 * 60) / (accel_time * 214.577) 
        
        # if self.ID == 1:
        #     print("%3d," %(self.ID), "%3d :" %(goal_index), int(max_velocity), int(acceleration))
        # return int(max_velocity), int(acceleration)
        return total_time, accel_time

# Setup all Dynamixels        
DXL = [0]*0
def setupDynamixels():
    for dxl_index in range(0, num_dxls):
        DXL.append(Dxls(DXL_INFO_ALL[dxl_index][0][0]))
        for goal_index in range(0, len(DXL_INFO_ALL[0][0]) - 2):
            # print(goal_index + 2)
            DXL[dxl_index].DXL_GOAL_POSITION_VALUE.append(DXL_INFO_ALL[dxl_index][0][goal_index + 2])

def isMoving(portHandler):
    value = 1
    for dxl_index in range(num_dxls):
        moving_status, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_MOVING)
        if moving_status:
            value = 0

    return value

# Enable Dynamixel Torque
def enableTorque(portHandler):
    for dxl_index in range(0, num_dxls):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)       
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID)
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID)
        # else:
        #     print("Dynamixel %d has been successfully connected" % (DXL[dxl_index].ID))


# time.sleep(8)
def walk(portHandler, num_steps):
    t1 = time.time()
    setupDynamixels()    
    
    enableTorque(portHandler)

    # x = []
    # y = []
    # Initialize GroupSyncWrite instance
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)
      
    for dxl_index in range(num_dxls):
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_P_GAIN_POSITION, 1500)
        if dxl_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID, 'p_gain')
        elif dxl_error != 0:
            print(packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID, 'p_gain')
            # Write Profile Velocity
        prof_vel, prof_acc = DXL[dxl_index].profileVel()
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PROFILE_VELOCITY, prof_vel)    
        if dxl_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID, 'vel')
        elif dxl_error != 0:
            print(packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID, 'vel')
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PROFILE_ACCELERATION, prof_acc)
        if dxl_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(dxl_comm_result), DXL[dxl_index].ID, 'acc')
        elif dxl_error != 0:
            print(packetHandler.getRxPacketError(dxl_error), DXL[dxl_index].ID, 'acc')

    for i in range(num_steps):

        for goal_index in range(len(DXL_INFO_ALL[0][0]) - 3, 5, -1):
                           
          #Write goal position
            #Add all Dynamixels' goal position value to groupSyncWrite parameter storage
            for dxl_index in range(num_dxls):
                    
                # Allocate goal position value into byte array
                param_goal_position = [DXL_LOBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_LOBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index]))]
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
            
        #     # while 1:
        #     #     present_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 1, 128)
        #     #     t2 = time.time()
        #     #     print(present_vel)
        #     #     if present_vel < 5000:
        #     #         x.append(t2-t1)
        #     #         y.append(present_vel)
        #     #     if present_vel == 0:
        #     #         break

        #     # print()
        #     # for dxl_index in range(num_dxls):
        #     #     present_pos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PRESENT_POSITION)
        #     #     error = DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index] - present_pos

        #     #     print("%.2d : %d" %(DXL[dxl_index].ID, error))
        #     # print()

        # # time.sleep(0.3)            
        # # dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_P_GAIN_POSITION, 850)
        # # if dxl_comm_result != COMM_SUCCESS:
        # #     print(packetHandler.getTxRxResult(dxl_comm_result), 1, 'p_gain')
        # # elif dxl_error != 0:
        # #     print(packetHandler.getRxPacketError(dxl_error), 1, 'p_gain')

        # for goal_index in range(6 , -1, -1):

        #   # Write goal position
        #     # Add all Dynamixels' goal position value to groupSyncWrite parameter storage
        #     for dxl_index in range(num_dxls):
                    
        #         # Allocate goal position value into byte array
        #         param_goal_position = [DXL_LOBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_LOBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index]))]
                
        #         dxl_addparam_result = groupSyncWrite.addParam(DXL[dxl_index].ID, param_goal_position)
        #         if dxl_addparam_result != 1:
        #             print("[ID:%03d] groupSyncWrite addparam failed" % (DXL[dxl_index].ID))
        #             quit()  
            
        #     # SyncWrite goal position
        #     dxl_comm_result = groupSyncWrite.txPacket()
        #     if dxl_comm_result != COMM_SUCCESS:
        #         print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        #     # Clear SyncWrite parameter storage
        #     groupSyncWrite.clearParam()
            time.sleep(0.3)


            # while 1:
            #     present_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 1, 128)
            #     t2 = time.time()
            #     print(present_vel)
            #     if present_vel < 5000:
            #         x.append(t2-t1)
            #         y.append(present_vel)
            #     if present_vel == 0:
            #         break
            
            # print()
            
        # for goal_index in range(len(DXL_INFO_ALL[0][0]) - 3, -1, -1):
            # for dxl_index in range(num_dxls):
            #     present_pos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL[dxl_index].ID, ADDR_MX_PRESENT_POSITION)
            #     error = DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index] - present_pos

            #     print("%.2d : %d" %(DXL[dxl_index].ID, error))
            # print()
            # # if goal_index == 14:
            #     time.sleep(0.3)
            # else:
            #     time.sleep(0.3)
        # time.sleep(0.05)
    # plt.plot(x, y)
    # plt.show()
        goal_index = 0
        for dxl_index in range(num_dxls):
                    
            # Allocate goal position value into byte array
            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_LOWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_LOBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index])), DXL_HIBYTE(DXL_HIWORD(DXL[dxl_index].DXL_GOAL_POSITION_VALUE[goal_index]))]
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


    t2 = time.time()
    print(t2 - t1)

    while 1:
        if isMoving(portHandler):
            # print('fo')
            break

    t2 = time.time()
    print(t2 - t1)
