#!/usr/bin/env python

# Author: Madhur Deep Jain

from dynamixel_sdk import *                   # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24                 # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36

PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600

NUM_DEVICES                 = 1
DEVICENAME                  = ['/dev/ttyUSB0']
DXL_BEG_ID                  = [1]
DXL_END_ID                  = [20]

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

portHandler   = [None]*NUM_DEVICES
packetHandler = [None]*NUM_DEVICES

for device_index in range(0, NUM_DEVICES):
    # Initialize PortHandler instance
    portHandler[device_index] = PortHandler(DEVICENAME[device_index])

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler[device_index] = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler[device_index].openPort():
        print("Succeeded to open the port %s" % (DEVICENAME[device_index]))
    else:
        print("Failed to open the port %s" % (DEVICENAME[device_index]))
        print("Press any key to terminate...")
        getch()
        quit()


    # Set port baudrate
    if portHandler[device_index].setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate of %s" % (DEVICENAME[device_index]))
    else:
        print("Failed to change the baudrate of %s" % (DEVICENAME[device_index]))
        print("Press any key to terminate...")
        getch()
        quit()

    for dxl_index in range(DXL_BEG_ID[device_index], DXL_END_ID[device_index]+1):
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler[device_index].read2ByteTxRx(portHandler[device_index], dxl_index, ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result==COMM_SUCCESS and dxl_error==0:
            print("\nDynamixel with [ID:%03d] has been successfully connected on %s\nPresPos:%03d" % (dxl_index, DEVICENAME[device_index], dxl_present_position))
        # Disable Dynamixel Torque
        '''dxl_comm_result, dxl_error = packetHandler[device_index].write1ByteTxRx(portHandler[device_index], dxl_index, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler[device_index].getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler[device_index].getRxPacketError(dxl_error))'''
