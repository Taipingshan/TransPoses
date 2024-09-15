from process import sync_imu_process
import torch
from net import TransPoseNet
from config import paths
from utils import normalize_and_concat
import articulate as art



# folder_path = './input/test3'
# total_imu_acc_tensor, total_imu_rm_tensor = total_imu_process(folder_path, num_frames=4000, num_imu=6)
# folder_path = './input/noitom_test/noitom3.csv'
folder_path = './input/20240912_204806_sensor.csv'
# folder_path = './noitom/combined_file.csv'
total_imu_acc_tensor, total_imu_rm_tensor = sync_imu_process(folder_path, num_frames=4000, num_imu=6)

# print(total_imu_acc_tensor)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
net = TransPoseNet().to(device)
# acc = torch.load(os.path.join(paths.example_dir, 'acc.pt'))
# ori = torch.load(os.path.join(paths.example_dir, 'ori.pt'))

acc = total_imu_acc_tensor.float().transpose(0, 1)

ori = total_imu_rm_tensor.float().transpose(0, 1)

# torch.save(acc, './output/tensor/acc.pt')
# torch.save(ori, './output/tensor/ori.pt')
# print(ori.size())
x = normalize_and_concat(acc, ori).to(device)  # torch.Size([1760, 72])

pose, tran = net.forward_offline(x)     # offline
# pose, tran = [torch.stack(_) for _ in zip(*[net.forward_online(f) for f in x])]   # online

art.ParametricModel(paths.smpl_file).view_motion([pose], [tran])