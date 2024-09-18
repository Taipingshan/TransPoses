import pandas as pd
import csv
import os
from itertools import islice

# 读取原始CSV文件
df = pd.read_csv('71425_contrast.csv',)

# print(df)
# LeftForeArm
# 选择需要保存的列
selected_columns1 = ['LeftForeArm-Sensor-Acce-x', 'LeftForeArm-Sensor-Acce-y', 'LeftForeArm-Sensor-Acce-z',
                     'LeftForeArm-Sensor-Gyro-x', 'LeftForeArm-Sensor-Gyro-y',
                     'LeftForeArm-Sensor-Gyro-z']  # 替换为你需要保存的列名

# selected_columns1 = ['LeftArm-Sensor-Acce-x', 'LeftArm-Sensor-Acce-y', 'LeftArm-Sensor-Acce-z',
#                      'LeftArm-Sensor-Gyro-x', 'LeftArm-Sensor-Gyro-y',
#                      'LeftArm-Sensor-Gyro-z']  # 替换为你需要保存的列名
# 创建包含选定列的新DataFrame
new_df1 = df[selected_columns1]

# 重命名列
new_column_names1 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df1 = new_df1.rename(columns=dict(zip(selected_columns1, new_column_names1)))

# 将新DataFrame保存为新的CSV文件
new_df1.to_csv('file1.csv', index=False)


## RightForeArm
# 选择需要保存的列
selected_columns2 = ['RightForeArm-Sensor-Acce-x', 'RightForeArm-Sensor-Acce-y', 'RightForeArm-Sensor-Acce-z',
                     'RightForeArm-Sensor-Gyro-x', 'RightForeArm-Sensor-Gyro-y',
                     'RightForeArm-Sensor-Gyro-z']  # 替换为你需要保存的列名

# 创建包含选定列的新DataFrame
new_df2 = df[selected_columns2]

# 重命名列
new_column_names2 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df2 = new_df2.rename(columns=dict(zip(selected_columns2, new_column_names2)))

# 将新DataFrame保存为新的CSV文件
new_df2.to_csv('file2.csv', index=False)


## LeftLeg
# 选择需要保存的列
selected_columns3 = ['LeftLeg-Sensor-Acce-x', 'LeftLeg-Sensor-Acce-y', 'LeftLeg-Sensor-Acce-z',
                     'LeftLeg-Sensor-Gyro-x', 'LeftLeg-Sensor-Gyro-y', 'LeftLeg-Sensor-Gyro-z']  # 替换为你需要保存的列名

# 创建包含选定列的新DataFrame
new_df3 = df[selected_columns3]

# 重命名列
new_column_names3 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df3 = new_df3.rename(columns=dict(zip(selected_columns3, new_column_names3)))

# 将新DataFrame保存为新的CSV文件
new_df3.to_csv('file3.csv', index=False)


## RightLeg
# 选择需要保存的列
selected_columns4 = ['RightLeg-Sensor-Acce-x', 'RightLeg-Sensor-Acce-y', 'RightLeg-Sensor-Acce-z',
                    'RightLeg-Sensor-Gyro-x', 'RightLeg-Sensor-Gyro-y', 'RightLeg-Sensor-Gyro-z']  # 替换为你需要保存的列名


# 创建包含选定列的新DataFrame
new_df4 = df[selected_columns4]

# 重命名列
new_column_names4 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df4 = new_df4.rename(columns=dict(zip(selected_columns4, new_column_names4)))

# 将新DataFrame保存为新的CSV文件
new_df4.to_csv('file4.csv', index=False)


## Head
# 选择需要保存的列
selected_columns5 = ['Head-Sensor-Acce-x', 'Head-Sensor-Acce-y', 'Head-Sensor-Acce-z',
                    'Head-Sensor-Gyro-x', 'Head-Sensor-Gyro-y', 'Head-Sensor-Gyro-z']  # 替换为你需要保存的列名


# 创建包含选定列的新DataFrame
new_df5 = df[selected_columns5]

# 重命名列
new_column_names5 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df5 = new_df5.rename(columns=dict(zip(selected_columns5, new_column_names5)))

# 将新DataFrame保存为新的CSV文件
new_df5.to_csv('file5.csv', index=False)


## Hips
# 选择需要保存的列
selected_columns6 = ['Hips-Sensor-Acce-x', 'Hips-Sensor-Acce-y', 'Hips-Sensor-Acce-z',
                    'Hips-Sensor-Gyro-x', 'Hips-Sensor-Gyro-y', 'Hips-Sensor-Gyro-z']  # 替换为你需要保存的列名


# 创建包含选定列的新DataFrame
new_df6 = df[selected_columns6]

# 重命名列
new_column_names6 = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']  # 替换为你想要的新列名
new_df6 = new_df6.rename(columns=dict(zip(selected_columns6, new_column_names6)))

# 将新DataFrame保存为新的CSV文件
new_df6.to_csv('file6.csv', index=False)


files = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv', 'file6.csv']


def count_csv_rows(file_path):
    # 打开CSV文件
    with open(file_path, 'r') as file:
        # 创建CSV阅读器
        reader = csv.reader(file)
        # 计算行数，减去标题行（如果有的话）
        row_count = sum(1 for row in reader) - 1
    return row_count


row_count = count_csv_rows(files[0])

with open('combined_file.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for line_number in range(1, row_count):
        for f in files:
            with open(f, newline='') as infile:
                reader = csv.reader(infile)
                for row in islice(reader, line_number - 1, line_number):
                    # 处理特定行数据
                    # print(row)
                    row = next(reader)
                writer.writerow(row)

header = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']

# 读取未带标题行的CSV文件
with open('combined_file.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

    # 在数据前插入标题行
data.insert(0, header)

with open('combined_file.csv', 'w', newline='') as file:
    # 将带有标题行的数据写入新的.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("已成功将六个IMU数据导入到combined_file.csv文件中。")


# 遍历文件列表
folder_path = os.getcwd()
for file_name in files:
    if file_name.endswith(".csv"):  # 检查文件扩展名是否为.csv
        file_path = os.path.join(folder_path, file_name)  # 构建完整的文件路径

        # 删除文件
        os.remove(file_path)
        print(f"已删除文件: {file_name}")