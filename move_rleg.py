#!/usr/bin/env python

# Author: Madhur Deep Jain

import os
import sys
import time

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
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVING_VELOCITY    = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = [14, 1, 2, 11, 16]                 # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_GOAL_POSITION_VALUE_14     = [3143,3145,3148,3151,3153,3155,3157,3159,3162,3164,3166,3167,3169,3171,3174,3176,3179,3181,3184,3187,3190,3193,3196,3198,3201,3203,3205,3206,3207,3208,3214,3221,3228,3235,3242,3249,3256,3262,3269,3275,3281,3288,3294,3299,3305,3311,3316,3322,3327,3333,3271,3221,3178,3140,3105,3074,3046,3021,2999,2981,2965,2954,2947,2944,2947,2956,2973,2999,3040,3106,3110,3113,3117,3120,3124,3128,3131,3134,3137,3140]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_1      = [652,649,645,641,637,632,628,623,618,614,612,611,611,610,611,611,611,612,613,615,616,617,618,619,619,619,618,617,614,610,615,620,624,629,634,639,644,648,652,655,659,663,666,669,671,673,676,678,680,682,576,494,428,373,326,287,255,231,213,202,198,201,213,233,263,304,359,431,530,678,676,674,672,670,669,666,664,662,659,655]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_2      = [607,613,620,626,633,639,646,653,660,667,670,672,675,677,680,682,684,686,687,689,691,692,694,696,698,700,703,706,710,714,716,718,720,722,724,726,729,731,733,736,739,741,744,747,751,754,757,761,764,768,812,843,866,883,896,904,907,907,903,895,884,869,850,828,800,768,730,684,627,545,550,556,561,567,572,578,583,589,595,601]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_11      = [3355,3348,3340,3333,3326,3319,3312,3306,3299,3294,3288,3283,3279,3275,3271,3268,3266,3264,3263,3263,3263,3263,3264,3266,3268,3271,3275,3279,3283,3288,3294,3299,3306,3312,3319,3326,3333,3340,3348,3355,3355,3363,3371,3378,3385,3392,3399,3405,3412,3417,3423,3428,3432,3436,3440,3443,3445,3447,3448,3448,3448,3448,3447,3445,3443,3440,3436,3432,3428,3423,3417,3412,3405,3399,3392,3385,3378,3371,3363,3355]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_16      = [240,247,255,262,269,276,283,289,296,301,307,312,316,320,324,327,329,331,332,332,332,332,331,329,327,324,320,316,312,307,301,296,289,283,276,269,262,255,247,240,240,232,224,217,210,203,196,190,183,178,172,167,163,159,155,152,150,148,147,147,147,147,148,150,152,155,159,163,167,172,178,183,190,196,203,210,217,224,232,240]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_VELOCITY         = [50, 50, 50, 50, 50, 50]
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

for dxl_index in range(0, 5):
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[dxl_index], ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID[dxl_index], ADDR_MX_MOVING_VELOCITY, DXL_MOVING_VELOCITY[dxl_index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel %d has been successfully connected" % (DXL_ID[dxl_index]))

# time.sleep(8)

for goal_index in range(0,80):
    # Write goal position
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 14, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_14[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_1[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 2, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_2[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 11, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_11[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 16, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_16[goal_index])
    # time.sleep(0.5)
    # Read present position
    dxl_moving_velocity, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, 1, ADDR_MX_MOVING_VELOCITY)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("%03d\n" % (dxl_moving_velocity))

    # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, DXL_GOAL_POSITION_VALUE, dxl_present_position))

    # if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
    #     break

# Disable Dynamixel Torque
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
