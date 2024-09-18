import os
import torch
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from scipy import signal
from scipy.signal import lfilter
import csv

# 定义保存的文件路径
csv_file = 'acc_data_after_filter.csv'
csv_ori_file = 'ori_data.csv'
csv_gyr_file = 'gyr_data.csv'


# 使用 csv 模块将数据写入 CSV 文件

def adaptive_filter(data, window_size):
    filtered_data = []
    for i in range(len(data)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(i + window_size // 2 + 1, len(data))
        sub_data = data[start_idx:end_idx]
        filtered_value = np.mean(sub_data, axis=0)
        filtered_data.append(filtered_value)
    return filtered_data


def sync_imu_process(path, num_frames=3000, num_imu=6):
    data = pd.read_csv('./input/20240912_204806_sensor.csv')

    acc_data = data.loc[:, ['AccX', 'AccY', 'AccZ']]
    acc_data = acc_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    acc_data = acc_data.dropna()
    # print(acc_data.shape)
    acc_data_list = acc_data.values.tolist()

    # 预处理acc_data_list中的数据
    # 自适应窗口滤波
    # acc_data_list = adaptive_filter(acc_data_list, 5)

    # 计算正数的平均数和负数的平均数
    # for dim in range(len(acc_data_list[0])):
    #     positive_mean = np.mean([data[dim] for data in acc_data_list if data[dim] >= 0])
    #     negative_mean = np.mean([data[dim] for data in acc_data_list if data[dim] < 0])
    #
    #     # 对每个维度的数据进行处理
    #     for i in range(len(acc_data_list)):
    #         for dim in range(len(acc_data_list[i])):
    #             if 0 <= acc_data_list[i][dim] < positive_mean:
    #                 acc_data_list[i][dim] /= 5.0
    #             elif 0 > acc_data_list[i][dim] > negative_mean:
    #                 acc_data_list[i][dim] /= 5.0

    # with open(csv_file, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(acc_data_list)

    acc_data_array = np.array(acc_data_list)
    acc_tensor = torch.tensor(acc_data_array).reshape(-1, 3)

    gyr_data = data.loc[:, ['GyrX', 'GyrY', 'GyrZ']]
    gyr_data = gyr_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    gyr_data = gyr_data.dropna()
    np.savetxt(csv_gyr_file, gyr_data, delimiter=',')
    # gyr_data_list = gyr_data.values.tolist()
    # time_interval = 1 / 60
    time_interval = 1 / 120
    rotation_vector = np.cumsum(gyr_data * time_interval, axis=1)  # 计算旋转向量
    rotation = Rotation.from_rotvec(rotation_vector)  # 创建Rotation对象
    orientation_matrix = rotation.as_matrix()  # 将旋转对象转换为方向矩阵

    # 将旋转角度保存
    # np.savetxt(csv_ori_file, orientation_matrix.reshape(-1, 3), delimiter=',')
    rm_tensor = torch.from_numpy(orientation_matrix).view(-1, 3, 3)

    if acc_tensor.size(0) > num_frames * 6:
        total_acc_tensor = torch.zeros(num_frames, 3)
        total_rm_tensor = torch.zeros(num_frames, 3, 3)
    else:
        total_acc_tensor = torch.zeros(int(acc_tensor.size(0) / 6), 3)
        total_rm_tensor = torch.zeros(int(rm_tensor.size(0) / 6), 3, 3)

    for i in range(num_imu):
        indices = torch.arange(i, acc_tensor.size(0), num_imu)
        # print(indices_i)
        acc_int_tensor = torch.index_select(acc_tensor, 0, indices)
        rm_int_tensor = torch.index_select(rm_tensor, 0, indices)
        if acc_tensor.size(0) > num_frames * 6:
            total_acc_tensor = torch.cat((total_acc_tensor, acc_int_tensor[:num_frames]))
            total_rm_tensor = torch.cat((total_rm_tensor, rm_int_tensor[:num_frames]))
        else:
            total_acc_tensor = torch.cat((total_acc_tensor, acc_int_tensor))
            total_rm_tensor = torch.cat((total_rm_tensor, rm_int_tensor))

    total_acc_tensor = total_acc_tensor.reshape(num_imu + 1, -1, 3)
    total_rm_tensor = total_rm_tensor.reshape(num_imu + 1, -1, 3, 3)
    total_acc_tensor = total_acc_tensor[1:]
    total_rm_tensor = total_rm_tensor[1:]

    return total_acc_tensor, total_rm_tensor
# print(total_acc_tensor.size())
# print(total_rm_tensor.size())
# print(new_tensor)
