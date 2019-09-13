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
ADDR_MX_TORQUE_ENABLE         = 64               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION         = 116
ADDR_MX_PRESENT_POSITION      = 132
ADDR_MX_PROFILE_VELOCITY      = 112
ADDR_MX_PROFILE_ACCELERATION  = 108

num_steps = int(sys.argv[2])
t_sub_steps = 0.001

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = [12, 13, 17, 15, 9, 14, 1, 2, 11, 16]                 # Dynamixel ID : 1
BAUDRATE                    = 57600              # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_GOAL_POSITION_VALUE_12     = [1678,1671,1665,1660,1654,1648,1643,1637,1632,1626,1688,1738,1781,1819,1854,1885,1913,1938,1960,1978,1994,2005,2012,2015,2012,2003,1986,1960,1919,1853,1849,1846,1842,1839,1835,1831,1828,1825,1822,1819,1816,1814,1811,1808,1806,1804,1802,1800,1797,1795,1793,1792,1790,1788,1785,1783,1780,1778,1775,1772,1769,1766,1763,1761,1758,1756,1754,1753,1752,1751,1745,1738,1731,1724,1717,1710,1703,1697,1690,1684]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_13     = [2246,2242,2239,2236,2234,2232,2229,2227,2225,2223,2329,2411,2477,2532,2579,2618,2650,2674,2692,2703,2707,2704,2692,2672,2642,2601,2546,2474,2375,2227,2229,2231,2233,2235,2236,2239,2241,2243,2246,2250,2253,2256,2260,2264,2268,2273,2277,2282,2287,2291,2293,2294,2294,2295,2294,2294,2294,2293,2292,2290,2289,2288,2287,2286,2286,2286,2287,2288,2291,2295,2290,2285,2281,2276,2271,2266,2261,2257,2253,2250]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_17     = [2915,2917,2920,2923,2927,2930,2933,2937,2940,2944,2988,3019,3042,3059,3072,3080,3083,3083,3079,3071,3060,3045,3026,3004,2976,2944,2906,2860,2803,2721,2726,2732,2737,2743,2748,2754,2759,2765,2771,2777,2783,2789,2796,2802,2809,2815,2822,2829,2836,2843,2846,2848,2851,2853,2856,2858,2860,2862,2863,2865,2867,2868,2870,2872,2874,2876,2879,2882,2886,2890,2892,2894,2896,2898,2900,2902,2905,2907,2909,2912]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_15     = [1689,1682,1674,1667,1660,1653,1646,1640,1633,1628,1622,1617,1613,1609,1605,1602,1600,1598,1597,1597,1597,1597,1598,1600,1602,1605,1609,1613,1617,1622,1628,1633,1640,1646,1653,1660,1667,1674,1682,1689,1689,1697,1705,1712,1719,1726,1733,1739,1746,1751,1757,1762,1766,1770,1774,1777,1779,1781,1782,1782,1782,1782,1781,1779,1777,1774,1770,1766,1762,1757,1751,1746,1739,1733,1726,1719,1712,1705,1697,1689]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_9      = [2108,2101,2093,2086,2079,2072,2065,2059,2052,2047,2041,2036,2032,2028,2024,2021,2019,2017,2016,2016,2016,2016,2017,2019,2021,2024,2028,2032,2036,2041,2047,2052,2059,2065,2072,2079,2086,2093,2101,2108,2108,2116,2124,2131,2138,2145,2152,2158,2165,2170,2176,2181,2185,2189,2193,2196,2198,2200,2201,2201,2201,2201,2200,2198,2196,2193,2189,2185,2181,2176,2170,2165,2158,2152,2145,2138,2131,2124,2116,2108]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_14     = [1292,1294,1297,1300,1302,1304,1306,1308,1311,1313,1315,1316,1318,1320,1323,1325,1328,1330,1333,1336,1339,1342,1345,1347,1350,1352,1354,1355,1356,1357,1363,1370,1377,1384,1391,1398,1405,1411,1418,1424,1430,1437,1443,1448,1454,1460,1465,1471,1476,1482,1420,1370,1327,1289,1254,1223,1195,1170,1148,1130,1114,1103,1096,1093,1096,1105,1122,1148,1189,1255,1259,1262,1266,1269,1273,1277,1280,1283,1286,1289]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_1      = [693,690,686,682,678,673,669,664,659,655,653,652,652,651,652,652,652,653,654,656,657,658,659,660,660,660,659,658,655,651,656,661,665,670,675,680,685,689,693,696,700,704,707,710,712,714,717,719,721,723,617,535,469,414,367,328,296,272,254,243,239,242,254,274,304,345,400,472,571,719,717,715,713,711,710,707,705,703,700,696]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_2      = [175,181,188,194,201,207,214,221,228,235,238,240,243,245,248,250,252,254,255,257,259,260,262,264,266,268,271,274,278,282,284,286,288,290,292,294,297,299,301,304,307,309,312,315,319,322,325,329,332,336,380,411,434,451,464,472,475,475,471,463,452,437,418,396,368,336,298,252,195,113,118,124,129,135,140,146,151,157,163,169]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_11     = [3388,3381,3373,3366,3359,3352,3345,3339,3332,3327,3321,3316,3312,3308,3304,3301,3299,3297,3296,3296,3296,3296,3297,3299,3301,3304,3308,3312,3316,3321,3327,3332,3339,3345,3352,3359,3366,3373,3381,3388,3388,3396,3404,3411,3418,3425,3432,3438,3445,3450,3456,3461,3465,3469,3473,3476,3478,3480,3481,3481,3481,3481,3480,3478,3476,3473,3469,3465,3461,3456,3450,3445,3438,3432,3425,3418,3411,3404,3396,3388]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_GOAL_POSITION_VALUE_16     = [286,279,271,264,257,250,243,237,230,225,219,214,210,206,202,199,197,195,194,194,194,194,195,197,199,202,206,210,214,219,225,230,237,243,250,257,264,271,279,286,286,294,302,309,316,323,330,336,343,348,354,359,363,367,371,374,376,378,379,379,379,379,378,376,374,371,367,363,359,354,348,343,336,330,323,316,309,302,294,286]           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_PROFILE_ACCELERATION       = [100]*10
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

for dxl_index in range(0, 10):
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[dxl_index], ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID[dxl_index], ADDR_MX_PROFILE_ACCELERATION, DXL_PROFILE_ACCELERATION[dxl_index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel %d has been successfully connected" % (DXL_ID[dxl_index]))

# time.sleep(8)

for i in range(num_steps):
    for goal_index in range(0,79):
        prof_vel_12 = int((((abs(DXL_GOAL_POSITION_VALUE_12[goal_index] - DXL_GOAL_POSITION_VALUE_12[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, ADDR_MX_PROFILE_VELOCITY, prof_vel_12)    
        prof_vel_13 = int((((abs(DXL_GOAL_POSITION_VALUE_13[goal_index] - DXL_GOAL_POSITION_VALUE_13[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, ADDR_MX_PROFILE_VELOCITY, prof_vel_13)    
        prof_vel_17 = int((((abs(DXL_GOAL_POSITION_VALUE_17[goal_index] - DXL_GOAL_POSITION_VALUE_17[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 17, ADDR_MX_PROFILE_VELOCITY, prof_vel_17)    
        prof_vel_15 = int((((abs(DXL_GOAL_POSITION_VALUE_15[goal_index] - DXL_GOAL_POSITION_VALUE_15[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, ADDR_MX_PROFILE_VELOCITY, prof_vel_15)    
        prof_vel_9  = int((((abs(DXL_GOAL_POSITION_VALUE_9[goal_index] - DXL_GOAL_POSITION_VALUE_9[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 9, ADDR_MX_PROFILE_VELOCITY, prof_vel_9)    
        prof_vel_14 = int((((abs(DXL_GOAL_POSITION_VALUE_14[goal_index] - DXL_GOAL_POSITION_VALUE_14[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, ADDR_MX_PROFILE_VELOCITY, prof_vel_14)    
        prof_vel_1  = int((((abs(DXL_GOAL_POSITION_VALUE_1[goal_index] - DXL_GOAL_POSITION_VALUE_1[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_PROFILE_VELOCITY, prof_vel_1)    
        prof_vel_2  = int((((abs(DXL_GOAL_POSITION_VALUE_2[goal_index] - DXL_GOAL_POSITION_VALUE_2[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 2, ADDR_MX_PROFILE_VELOCITY, prof_vel_2)    
        prof_vel_11 = int((((abs(DXL_GOAL_POSITION_VALUE_11[goal_index] - DXL_GOAL_POSITION_VALUE_11[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, ADDR_MX_PROFILE_VELOCITY, prof_vel_11)    
        prof_vel_16 = int((((abs(DXL_GOAL_POSITION_VALUE_16[goal_index] - DXL_GOAL_POSITION_VALUE_16[goal_index+1])/4095)*60)/t_sub_steps)/0.229)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, ADDR_MX_PROFILE_VELOCITY, prof_vel_16)
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 12, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel)) 
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 13, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 17, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 9, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 14, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 1, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 2, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 11, ADDR_MX_PROFILE_VELOCITY)
        print("%d, " % (dxl_prof_vel))
        dxl_prof_vel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 16, ADDR_MX_PROFILE_VELOCITY)
        print("%d\n" % (dxl_prof_vel))   
        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_12[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_13[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 17, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_17[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_15[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 9, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_9[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_14[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_1[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 2, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_2[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_11[goal_index])
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, ADDR_MX_GOAL_POSITION, DXL_GOAL_POSITION_VALUE_16[goal_index])
        # time.sleep(0.002)
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