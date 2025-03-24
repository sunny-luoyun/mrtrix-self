import numpy as np
from scipy.io import loadmat
from scipy.stats import pearsonr

# 加载.mat文件
mat_A = loadmat('/data/text/NET/Sham/S1/NetworkMatrix_Sub001.mat')
mat_B = loadmat('/data/text/NET/Sham/S1/NetworkMatrix_Sub002.mat')

# 假设矩阵存储在字典的某个键中，需要根据实际情况调整键名
# 例如，假设矩阵存储在键 'data' 中
A = mat_A['NetworkMatrix']
B = mat_B['NetworkMatrix']

# 检查矩阵维度是否一致
if A.shape != B.shape:
    raise ValueError("矩阵A和B的维度不一致，请检查输入文件。")

# 将矩阵转换为向量形式
vector_A = A.flatten()
vector_B = B.flatten()

# 计算皮尔逊相关系数
correlation, p_value = pearsonr(vector_A, vector_B)

# 格式化输出，保留10位小数
print(f"皮尔逊相关系数: {correlation}")
