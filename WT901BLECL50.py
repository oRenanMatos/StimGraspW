'''
Universidade Federal do Rio de Janeiro
            PEB/COPPE/UFRJ

Author: Wellington Pinheiro, MSc.
Advisor: Luciano Menegaldo, DSc.
---------------------------------
WT901BLECL serial signal treatment

'''

# def get_acc(datahex):  #calculate the acceleration from IMU data | index 0, 1 are the header.

#     axl = datahex[2]                                        
#     axh = datahex[3]
#     ayl = datahex[4]                                        
#     ayh = datahex[5]
#     azl = datahex[6]                                        
#     azh = datahex[7]
    
#     k_acc = 16.0*9.81
 
#     acc_x = (axh << 8 | axl) / 32768.0 * k_acc
#     acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
#     acc_z = (azh << 8 | azl) / 32768.0 * k_acc
#     if acc_x >= k_acc:
#         acc_x -= 2 * k_acc
#     if acc_y >= k_acc:
#         acc_y -= 2 * k_acc
#     if acc_z >= k_acc:
#         acc_z-= 2 * k_acc
    
#     return acc_x,acc_y,acc_z

# def get_gyro(datahex):                                      
#     wxl = datahex[8]                                        
#     wxh = datahex[9]
#     wyl = datahex[10]                                        
#     wyh = datahex[11]
#     wzl = datahex[12]                                        
#     wzh = datahex[13]
#     k_gyro = 2000.0
 
#     gyro_x = (wxh << 8 | wxl) / 32768.0 * k_gyro
#     gyro_y = (wyh << 8 | wyl) / 32768.0 * k_gyro
#     gyro_z = (wzh << 8 | wzl) / 32768.0 * k_gyro
#     if gyro_x >= k_gyro:
#         gyro_x -= 2 * k_gyro
#     if gyro_y >= k_gyro:
#         gyro_y -= 2 * k_gyro
#     if gyro_z >=k_gyro:
#         gyro_z-= 2 * k_gyro
#     return gyro_x,gyro_y,gyro_z
 
 
# def get_angle(datahex):                                 
#     rxl = datahex[14]                                        
#     rxh = datahex[15]
#     ryl = datahex[16]                                        
#     ryh = datahex[17]
#     rzl = datahex[18]                                        
#     rzh = datahex[19]
#     k_angle = 180.0
 
#     angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
#     angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
#     angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
#     if angle_x >= k_angle:
#         angle_x -= 2 * k_angle
#     if angle_y >= k_angle:
#         angle_y -= 2 * k_angle
#     if angle_z >=k_angle:
#         angle_z-= 2 * k_angle
 
#     return angle_x,angle_y,angle_z

def writeCSVFile(data, experimentalInfo):
    from datetime import datetime
    import numpy as np
    import pandas as pd
    import csv

    try: 

        # Session Information Inputs
        experimentalInfo['PatientID'] = input("Patient ID: ")
        experimentalInfo['PatientAge'] = input("Patient Age: ")
        experimentalInfo['diseaselabel'] = input("Disease Label (i.e. PD, ET, Holmes): ")
        experimentalInfo['affectedArm'] = input("Affected Arm (i.e. Right = RA, Left = LA): ")
        experimentalInfo['medicine'] = input("Medicine (i.e. ON, OFF): ")
        experimentalInfo['task'] = input("Task (i.e. Rest, Posture, Spiral): ")
        experimentalInfo['trial'] = input("Trial (i.e. 01, 02, 03, 04, 05): ") 
        experimentalInfo['date'] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        experimentalInfo['TCLE#'] = input("TCLE#: ") 
        experimentalInfo['ProtocolType'] = input("Protocol Type (i.e. Placebo, OL Cocontraction, CL out of phase, etc): ")   


        #Get the current date and time
        current_date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        #Create a file name
        csv_file_name = current_date +'_patient_#'+experimentalInfo['PatientID']+'_'+ experimentalInfo['diseaselabel']+'_'+'IMUdata.csv'

        # Header info to CSV file (all experimental info)
        with open(csv_file_name, 'w', newline="") as f:
            writer = csv.writer(f, delimiter=':')
            for key, value in experimentalInfo.items():
                writer.writerow([key, value])
             

        #Header
        headerline = ['Time (s)', 'acc_x (m/s^2)', 'acc_y (m/s^2)', 'acc_z (m/s^2)', 'gyro_x (deg/s)', 'gyro_y (deg/s)', 'gyro_z (deg/s)', 'angle_x (deg)', 'angle_y (deg)', 'angle_z (deg)']

        #Save the data in a csv file
        pd.DataFrame(data).to_csv(csv_file_name, mode='a', header=headerline, sep='|', index=False)




    except:
        print('Error saving data')

    return


def getMotionData(datahex, currTime):
    import time

    axl = datahex[2]                                        
    axh = datahex[3]
    ayl = datahex[4]                                        
    ayh = datahex[5]
    azl = datahex[6]                                        
    azh = datahex[7]
    wxl = datahex[8]                                        
    wxh = datahex[9]
    wyl = datahex[10]                                        
    wyh = datahex[11]
    wzl = datahex[12]                                        
    wzh = datahex[13]
    rxl = datahex[14]                                        
    rxh = datahex[15]
    ryl = datahex[16]                                        
    ryh = datahex[17]
    rzl = datahex[18]                                        
    rzh = datahex[19]

    now=time.time() - currTime

    k_acc = 16.0*9.81
    k_gyro = 2000.0
    k_angle = 180.0

    acc_x = (axh << 8 | axl) / 32768.0 * k_acc
    acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
    acc_z = (azh << 8 | azl) / 32768.0 * k_acc
    if acc_x >= k_acc:
        acc_x -= 2 * k_acc
    if acc_y >= k_acc:
        acc_y -= 2 * k_acc
    if acc_z >= k_acc:
        acc_z-= 2 * k_acc


    gyro_x = (wxh << 8 | wxl) / 32768.0 * k_gyro
    gyro_y = (wyh << 8 | wyl) / 32768.0 * k_gyro
    gyro_z = (wzh << 8 | wzl) / 32768.0 * k_gyro
    if gyro_x >= k_gyro:
        gyro_x -= 2 * k_gyro
    if gyro_y >= k_gyro:
        gyro_y -= 2 * k_gyro
    if gyro_z >=k_gyro:
        gyro_z-= 2 * k_gyro


    angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle # Using manufacturer's Kalman filter
    angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >=k_angle:
        angle_z-= 2 * k_angle

    MotionData = [now, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, angle_x, angle_y, angle_z]
    return MotionData