import numpy as np
from scipy.io import loadmat, savemat

# 加载数据
mat_data = loadmat('/Users/langqin/data/TI/S1/Results/ROIMap/invlength/Sub001_aal_invlength_ROIMAP.mat')
mat = mat_data['NetworkMatrix']

# 通过input动态获取用户输入的行和列索引
user_input_rows = input("请输入要保留的行索引（用逗号分隔）：")
user_input_cols = input("请输入要保留的列索引（用逗号分隔）：")

# 将用户输入的字符串转换为整数列表，并减去1以适配Python的索引
rows_to_keep = [int(i) - 1 for i in user_input_rows.split(",")]
cols_to_keep = [int(i) - 1 for i in user_input_cols.split(",")]

# 提取指定的行和列
new_matrix = mat[np.ix_(rows_to_keep, cols_to_keep)]

# 删除全为0的行和列
new_matrix = new_matrix[~np.all(new_matrix == 0, axis=1)]  # 删除全为0的行
new_matrix = new_matrix[:, ~np.all(new_matrix == 0, axis=0)]  # 删除全为0的列

# 保存为.mat文件
output_file_mat = '/Users/langqin/data/TI/S1/Results/ROIMap/invlength/Sub001_aal_invlength_ROIMAP.mat'  # 指定保存路径
savemat(output_file_mat, {'NetworkMatrix': new_matrix})  # 保存为字典格式

# 输出结果
print("Original matrix shape:", mat.shape)
print("New matrix shape:", new_matrix.shape)
print("New matrix saved to:", output_file_mat)