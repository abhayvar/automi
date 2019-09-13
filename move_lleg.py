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

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = [12, 13, 17, 15, 9]                 # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_GOAL_POSITION_VALUE_12     = [1296,1289,1283,1278,1272,1266,1261,1255,1250,1244,1306,1356,1399,1437,1472,1503,1531,1556,1578,1596,1612,1623,1630,1633,1630,1621,1604,1578,1537,1471,1467,1464,1460,1457,1453,1449,1446,1443,1440,1437,1434,1432,1429,1426,1424,1422,1420,1418,1415,1413,1411,1410,1408,1406,1403,1401,1398,1396,1393,1390,1387,1384,1381,1379,1376,1374,1372,1371,1370,1369,1363,1356,1349,1342,1335,1328,1321,1315,1308,1302]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_13     = [1338,1334,1331,1328,1326,1324,1321,1319,1317,1315,1421,1503,1569,1624,1671,1710,1742,1766,1784,1795,1799,1796,1784,1764,1734,1693,1638,1566,1467,1319,1321,1323,1325,1327,1328,1331,1333,1335,1338,1342,1345,1348,1352,1356,1360,1365,1369,1374,1379,1383,1385,1386,1386,1387,1386,1386,1386,1385,1384,1382,1381,1380,1379,1378,1378,1378,1379,1380,1383,1387,1382,1377,1373,1368,1363,1358,1353,1349,1345,1342]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_17     = [2894,2896,2899,2902,2906,2909,2912,2916,2919,2923,2967,2998,3021,3038,3051,3059,3062,3062,3058,3050,3039,3024,3005,2983,2955,2923,2885,2839,2782,2700,2705,2711,2716,2722,2727,2733,2738,2744,2750,2756,2762,2768,2775,2781,2788,2794,2801,2808,2815,2822,2825,2827,2830,2832,2835,2837,2839,2841,2842,2844,2846,2847,2849,2851,2853,2855,2858,2861,2865,2869,2871,2873,2875,2877,2879,2881,2884,2886,2888,2891]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_15     = [1730,1723,1715,1708,1701,1694,1687,1681,1674,1669,1663,1658,1654,1650,1646,1643,1641,1639,1638,1638,1638,1638,1639,1641,1643,1646,1650,1654,1658,1663,1669,1674,1681,1687,1694,1701,1708,1715,1723,1730,1730,1738,1746,1753,1760,1767,1774,1780,1787,1792,1798,1803,1807,1811,1815,1818,1820,1822,1823,1823,1823,1823,1822,1820,1818,1815,1811,1807,1803,1798,1792,1787,1780,1774,1767,1760,1753,1746,1738,1730]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_9      = [3335,3342,3350,3357,3364,3371,3378,3384,3391,3396,3402,3407,3411,3415,3419,3422,3424,3426,3427,3427,3427,3427,3426,3424,3422,3419,3415,3411,3407,3402,3396,3391,3384,3378,3371,3364,3357,3350,3342,3335,3335,3327,3319,3312,3305,3298,3291,3285,3278,3273,3267,3262,3258,3254,3250,3247,3245,3243,3242,3242,3242,3242,3243,3245,3247,3250,3254,3258,3262,3267,3273,3278,3285,3291,3298,3305,3312,3319,3327,3335]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
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
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel %d has been successfully connected" % (DXL_ID[dxl_index]))

# time.sleep(8)

for goal_index in range(0,80):
    # Write goal position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_12[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_13[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 17, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_17[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_15[goal_index])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 9, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_9[goal_index])
    time.sleep(0.1)
    # Read present position
    # dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print("%s" % packetHandler.getRxPacketError(dxl_error))

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
