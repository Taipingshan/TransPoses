import pandas as pd

# 读取CSV文件为DataFrame对象
df = pd.read_csv('1.csv', encoding='utf-8')

# 按第一列升序排序，再按第二列升序排序
data = df.sort_values([' FrameNumber', 'SensorId'], ascending=[True, True])

#把新的数据写入文件
data.to_csv('result.csv', mode='a+', index=False)