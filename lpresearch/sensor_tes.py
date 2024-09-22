import pandas as pd

import matplotlib.pyplot as plt

#csv文件读取
path = 'data/sensor_test/20240921_213506_EF.csv'
data = pd.read_csv(path)

#3加速度数据读取
time = data['TimeStamp']
AccX = data['AccX']
AccY = data['AccY']
AccZ = data['AccZ']

frame_num = AccX.shape[0]

v_cum = []
x_cum = []
v = 0
x = 0


for i in range(0,frame_num-1):
    
    v = v + AccZ[i]*1/100
    x = x + v*1/100
    v_cum.append(v)
    x_cum.append(x)


time = time[1:]

plt.plot(time,v_cum)
plt.show()



