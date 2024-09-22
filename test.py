import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def sensor_test(acc,fre):
    frame_num = acc.shape[0]

    v_cum = [0]
    x_cum = [0]
    v = 0
    x = 0

    for i in range(0,frame_num-1):
    
        v = v + acc[i]*1/fre
        x = x + v*1/fre
        v_cum.append(v)
        x_cum.append(x)
    return [v_cum,x_cum]





#csv文件读取
path = 'data/sensor_test/20240922_215247_10.csv'
data = pd.read_csv(path)

#3加速度数据读取
time = data['TimeStamp']
AccX = data['AccX']
AccY = data['AccY']
AccZ = data['AccZ']


[vx,X] = sensor_test(AccX,400)
[vy,Y] = sensor_test(AccY,400)
[vz,Z] = sensor_test(AccX,400)


plt.subplot(1,3,1)
plt.plot(time,X)

plt.subplot(1,3,2)
plt.plot(time,Y)

plt.subplot(1,3,3)
plt.plot(time,Z)

plt.show()


# 输入加速度数据，输出速度v，位移x



