import pandas as pd

# 读取原始CSV文件
df = pd.read_csv('raw1.csv')

# 选择需要保存的列
selected_columns = ['Hips-Sensor-Acce-x', 'Hips-Sensor-Acce-y', 'Hips-Sensor-Acce-z',
                    'Hips-Sensor-Gyro-x', 'Hips-Sensor-Gyro-y', 'Hips-Sensor-Gyro-z']  # 替换为你需要保存的列名


# 创建包含选定列的新DataFrame
new_df = df[selected_columns]

# 重命名列
new_column_names = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df = new_df.rename(columns=dict(zip(selected_columns, new_column_names)))

# 将新DataFrame保存为新的CSV文件
new_df.to_csv('file6.csv', index=False)