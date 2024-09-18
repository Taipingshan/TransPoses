import sys, os
from collections import OrderedDict
from datetime import datetime
import time
import threading
import multiprocessing
import csv
#import keyboard
import numpy as np

from lpmslib import LpmsB2
from lpmslib import lputils

TAG = "MAIN"

def readSensorData2CSV(sensorIDstr, port, Global,Mydata):
    TAG = sensorIDstr
    baudrate = 115200
        
       
    # Connect to sensor
    sensor = LpmsB2.LpmsB2(port, Global['baudrate'])
    lputils.logd(TAG, "Connecting sensor " + sensorIDstr)
    if not sensor.connect():
        return

    lputils.logd(TAG, "Connected")

    with open(''.join([Global['FilePrefix'], sensorIDstr, '.csv']), 'w') as f:
        myWriter = csv.writer(f, quoting=csv.QUOTE_ALL)

        # myWriter.writerow(['TimeStamp', 'FrameCounter', 'AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ',
        #                        'QuatW', 'QuatX', 'QuatY', 'QuatZ', 'EulerX', 'EulerY', 'EulerZ', 'LinAccX',
        #                        'LinAccY', 'LinAccZ'])
        # myWriter.writerow(['TimeStamp', 'FrameCounter', 'LinAccX', 'LinAccY', 'LinAccZ','QuatW', 'QuatX', 'QuatY', 'QuatZ'])
        myWriter.writerow(
            ['TimeStamp', 'FrameCounter', 'AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ'])
        # Set 16bit data to reduce amount of stream data
        sensor.set_16bit_mode()
        sensor.set_filter_mode()
        # Set stream frequency
        sensor.set_stream_frequency_120Hz()  #调整帧数

        # Put sensor in sync mode 
        sensor.start_sync()
        time.sleep(1)

        # Clear sensor internal data queue
        sensor.clear_data_queue()

        # Sensor ready
        Global[sensorIDstr] = True

        # Wait for sync signal
        while not Global['stopSync']:
            continue
        sensor.stop_sync()


        while not Global['quit']:
            sensor_data = sensor.get_stream_data()
            if not sensor_data:
                continue

            data = [sensor_data[1]*0.0025, 
                    sensor_data[2],
                    sensor_data[6][0], sensor_data[6][1], sensor_data[6][2],
                    sensor_data[7][0], sensor_data[7][1], sensor_data[7][2],
                    sensor_data[9][0], sensor_data[9][1], sensor_data[9][2], sensor_data[9][3],
                    sensor_data[10][0], sensor_data[10][1], sensor_data[10][2],
                    sensor_data[11][0], sensor_data[11][1], sensor_data[11][2]
                    ]
            # myWriter.writerow(data)

            tmpdata = [sensor_data[1]*0.0025,sensor_data[2],sensor_data[11][0], sensor_data[11][1], sensor_data[11][2],
                      sensor_data[7][0], sensor_data[7][1], sensor_data[7][2]]
            #print(sensorIDstr,Mydata)
            #print(np.array(Global['Mydata']).shape)
            if sensorIDstr == 'lpms1':
                Mydata[0].append(tmpdata)
            elif sensorIDstr == 'lpms2':
                Mydata[1].append(tmpdata)
            elif sensorIDstr == 'lpms3':
                Mydata[2].append(tmpdata)
            elif sensorIDstr == 'lpms4':
                Mydata[3].append(tmpdata)
            elif sensorIDstr == 'lpms5':
                Mydata[4].append(tmpdata)
            elif sensorIDstr == 'lpms6':
                Mydata[5].append(tmpdata)


        sensor.disconnect()

        lputils.logd(TAG, "Terminated")
   


def processdata(Global,Mydata):
    print('processing data...')
    with open(''.join([Global['FilePrefix'], 'sensor', '.csv']), 'w', newline="") as f:
        mWriter = csv.writer(f, quoting=csv.QUOTE_ALL)
        # mWriter.writerow(['TimeStamp', 'FrameCounter', 'AccX', 'AccY', 'AccZ', 'QuatW', 'QuatX', 'QuatY', 'QuatZ'])
        mWriter.writerow(
            ['TimeStamp', 'FrameCounter', 'AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ'])
        while not Global['quit']:
            if len(Mydata[0]) != 0 and len(Mydata[1]) != 0 and len(Mydata[2]) != 0 and len(Mydata[3]) != 0 and len(
                    Mydata[4]) != 0 and len(Mydata[5]) != 0:  # 只在这个进程里面进行处理
                Mytime = [Mydata[0][0][0], Mydata[1][0][0], Mydata[2][0][0],
                          Mydata[3][0][0], Mydata[4][0][0],Mydata[5][0][0]]
                if Mytime.count(Mytime[0]) == len(Mytime):  # 6个时间相等
                    print('lpms1', Mydata[0][0])
                    print('lpms2', Mydata[1][0])
                    print('lpms3', Mydata[2][0])
                    print('lpms4', Mydata[3][0])
                    print('lpms5', Mydata[4][0])
                    print('lpms6', Mydata[5][0])
                    mWriter.writerow(Mydata[0][0])
                    mWriter.writerow(Mydata[1][0])
                    mWriter.writerow(Mydata[2][0])
                    mWriter.writerow(Mydata[3][0])
                    mWriter.writerow(Mydata[4][0])
                    mWriter.writerow(Mydata[5][0])
                    del Mydata[0][0]
                    del Mydata[1][0]
                    del Mydata[2][0]
                    del Mydata[3][0]
                    del Mydata[4][0]
                    del Mydata[5][0]
                else:
                    maxIdx = Mytime.index(max(Mytime))
                    maxIdx = [maxIdx]
                    for i in range(6):
                        if i not in maxIdx:
                            del Mydata[i][0]



def elapsedTimePrinter(Global):
    start_time = time.time()
    while not Global['quit']:

        elapsed_time = time.time() - start_time
        print("\rElapsed time(s): %f\t"%(elapsed_time) ),
        time.sleep(.2)


def main():
    # Settings
    port2 = 'COM11'  #EF 右手 2
    port3 = 'COM13'  #62 左腿 3
    port4 = 'COM7'   #F3 右腿 4
    port5 = 'COM9'     #10 头  5
    port6 = 'COM6' #E3 腰 6
    port1 = 'COM3' #35 左手  1
    baudrate = 115200
    sensor2Id = 'lpms2' #EF 右手
    sensor3Id = 'lpms3' #62 左腿
    sensor4Id = 'lpms4' #F3 右腿
    sensor5Id = 'lpms5' #10 头
    sensor6Id = 'lpms6' #E3 腰
    sensor1Id = 'lpms1' #35 左手
    dateTime = datetime.now().strftime("%Y%m%d_%H%M%S_")

    manager = multiprocessing.Manager()
    Global = manager.dict()

    Global['quit'] = False
    Global['stopSync'] = False
    Global['baudrate'] = baudrate
    Global['FilePrefix'] = dateTime
    Global[sensor1Id] = False       # Sensor ready flag
    Global[sensor2Id] = False       # Sensor ready flag.
    Global[sensor3Id] = False  # Sensor ready flag
    Global[sensor4Id] = False  # Sensor ready flag
    Global[sensor5Id] = False  # Sensor ready flag
    Global[sensor6Id] = False  # Sensor ready flag
    data1 = manager.list()
    data2 = manager.list()
    data3 = manager.list()
    data4 = manager.list()
    data5 = manager.list()
    data6 = manager.list()
    Mydata = [data1,data2,data3,data4,data5,data6]

    # Start sensor thread
    p1 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor1Id, port1, Global,Mydata))
    p2 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor2Id, port2, Global,Mydata))
    p3 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor3Id, port3, Global,Mydata))
    p4 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor4Id, port4, Global,Mydata))
    p5 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor5Id, port5, Global,Mydata))
    p6 = multiprocessing.Process(target=readSensorData2CSV, args=(sensor6Id, port6, Global,Mydata))
    p7 = multiprocessing.Process(target=processdata,args=(Global,Mydata))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()

    # Wait for sensors to connect
    print("Waiting for sensor to connect")
    # while not Global[sensor1Id] and not Global[sensor2Id]and not Global[sensor3Id]and not Global[sensor4Id]and not Global[sensor5Id]and not Global[sensor6Id]:
    while not Global[sensor1Id] and not Global[sensor5Id] and not Global[sensor6Id] :
        time.sleep(2)

    # Sync and start data logging
    input("Sensors connected, Input enter to sync and start recording process")
    Global['stopSync'] = True
    print("Input enter to stop recording")
   # p3.start();

    # Wait for quit command
    input("")

    Global['quit'] = True

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    print("Bye")

if __name__ == "__main__":
    main()