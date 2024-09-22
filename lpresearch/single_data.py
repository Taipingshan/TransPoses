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
    #数据输出文件夹
    folder_path = "data/sensor_test/"
    file_name = ''.join([Global['FilePrefix'], sensorIDstr, '.csv'])
    path = os.path.join(folder_path,file_name)

    with open(path, 'w') as f:
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
        sensor.set_stream_frequency_400Hz()  #调整帧数

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
            Mydata.append(tmpdata)
            myWriter.writerow(Mydata[0])
            del Mydata[0]

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
            if len(Mydata[0]) != 0 :  # 只在这个进程里面进行处理
                Mytime = Mydata[0][0]
                mWriter.writerow(Mydata[0])
                del Mydata[0]


#


def elapsedTimePrinter(Global):

    start_time = time.time()
    while not Global['quit']:

        elapsed_time = time.time() - start_time
        print("\rElapsed time(s): %f\t"%(elapsed_time) ),
        time.sleep(.2)
        


def main():
    # Settings

    port = 'COM7' #35 左手  1
    baudrate = 115200
    sensorId = 'F3' 
    dateTime = datetime.now().strftime("%Y%m%d_%H%M%S_")

    manager = multiprocessing.Manager()
    Global = manager.dict()

    Global['quit'] = False
    Global['stopSync'] = False
    Global['baudrate'] = baudrate

    Global['FilePrefix'] = dateTime
    Global[sensorId] = False       # Sensor ready flag
    data = manager.list()

    Mydata = data

    # Start sensor thread
    p1 = multiprocessing.Process(target=readSensorData2CSV, args=(sensorId, port, Global,Mydata))

    # p7 = multiprocessing.Process(target=processdata,args=(Global,Mydata))

    p1.start()

    # p7.start()

    # Wait for sensors to connect
    print("Waiting for sensor to connect")
    # while not Global[sensor1Id] and not Global[sensor2Id]and not Global[sensor3Id]and not Global[sensor4Id]and not Global[sensor5Id]and not Global[sensor6Id]:
    while not Global[sensorId] :
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
    
    print("Bye")

if __name__ == "__main__":
    main()
    