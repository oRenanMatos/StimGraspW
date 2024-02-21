'''
Universidade Federal do Rio de Janeiro
            PEB/COPPE/UFRJ

Author: Wellington Pinheiro, MSc.
Advisor: Luciano Menegaldo, DSc.
---------------------------------
WT901BLECL routines of configuration and 
calibration of the IMU.

MIT License (2023)

'''
import time


def setSamplingFrequency(freq, ser):

    # Set the frequency of the IMU
    # RATE: return rate
    # 0x01: 0.1Hz
    # 0x02: 0.5Hz
    # 0x03: 1Hz
    # 0x04: 2Hz
    # 0x05: 5Hz
    # 0x06: 10Hz (default)
    # 0x07: 20Hz
    # 0x08: 50Hz
    # 0x09: 100Hz
    # 0x0a: 200Hz

    #comand to send
    if freq == 0.1:
        command='FFAA030100'
    elif freq == 0.5:
        command='FFAA030200'
    elif freq == 1:
        command='FFAA030300'
    elif freq == 2:
        command='FFAA030400'
    elif freq == 5:
        command='FFAA030500'
    elif freq == 10:
        command='FFAA030600'
    elif freq == 20:
        command='FFAA030700'
    elif freq == 50:
        command='FFAA030800'
    elif freq == 100:
        command='FFAA030900'
    elif freq == 200:
        command='FFAA030A00'
    else:
        print("Invalid frequency")
        return
    # Save Settings
    save='FFAA000000'
    # send command
    Fs_message =bytes.fromhex(command)
    save_message =bytes.fromhex(save)

    ser.write(Fs_message) # set new  sampling frequency
    ser.write(save_message) # save configuration

    #print(str(command))
    print("ajustando Fs para {:.2f}".format(freq))
    time.sleep(2)

    # Read the response from the IMU
    # ser.flushInput()
    # command ='FFAA270300'
    # readfreq =bytes.fromhex(command)
    # ser.write(readfreq)
    # time.sleep(0.1)
    # response = ser.read(ser.in_waiting)
    # print(response.hex()+"\n")
    # print("leitura registrador")
    # time.sleep(10)
    return

def listcom():
    #list devices connected to serial ports

    import serial
    
    import serial.tools.list_ports
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)

    if len(port_list) == 0:
        print('No port in use')
    else:
        for i in range(0,len(port_list)):
            print(port_list[i])

        return
    

def readTempIMU(ser):
    # Read the temperature of the IMU
    
    import re
    import WT901BLECL50 as IMU
    
    ser.flushInput()

    command ='FFAA274000'
    readtemp =bytes.fromhex(command)
    ser.write(readtemp)
    time.sleep(0.1)
    response = ser.read(ser.in_waiting)
    tl = response[4]
    th = response[5]
    IMUTemp = (th << 8 | tl) / 100

    print("IMU Temperature: {:.2f} C".format(IMUTemp))
    time.sleep(2)
    return


def ConfigDataHandle(response):
    
    #function to print on the terminal IMU raw response
    
    import re

    # Handling multiple readings in one chunk
    response_str = response.hex() #convert to string
    split_hex = re.split("(?=5571)", response_str) #5571 is the header of the IMU data other than standard
    meas_length = 40
    measurements=[]

    for part in split_hex:
                if len(part) >= meas_length:
                    measurement = part[:meas_length]
                    print(measurement)

    return
