import os
import re
import pandas as pd
import scipy.io as sio
from scipy.stats import pearsonr
import numpy as np

def find_matching_files(root_dir):
    """
    递归遍历文件夹，找到所有匹配的文件路径
    """
    pair_folders = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    matching_files = []

    # 遍历每个pair文件夹
    for pair in pair_folders:
        pair_path = os.path.join(root_dir, pair)
        group_folders = [d for d in os.listdir(pair_path) if os.path.isdir(os.path.join(pair_path, d))]

        # 遍历每个group文件夹
        for group in group_folders:
            group_path = os.path.join(pair_path, group)
            condition_folders = [d for d in os.listdir(group_path) if os.path.isdir(os.path.join(group_path, d))]

            # 遍历每个condition文件夹
            for condition in condition_folders:
                condition_path = os.path.join(group_path, condition)
                mat_files = [f for f in os.listdir(condition_path) if f.endswith('.mat')]

                # 将文件路径存储为元组 (pair, group, condition, filename)
                for mat_file in mat_files:
                    matching_files.append((pair, group, condition, os.path.join(condition_path, mat_file)))

    return matching_files



def perform_correlation_analysis(file1, file2):
    """
    执行相关性分析并返回皮尔逊相关系数，忽略值为0的数据
    """
    mat_A = sio.loadmat(file1)
    mat_B = sio.loadmat(file2)

    # 假设矩阵存储在字典的某个键中，需要根据实际情况调整键名
    A = mat_A['NetworkMatrix']
    B = mat_B['NetworkMatrix']

    # 检查矩阵维度是否一致
    if A.shape != B.shape:
        raise ValueError("矩阵A和B的维度不一致，请检查输入文件。")

    # 将矩阵转换为向量形式
    vector_A = A.flatten()
    vector_B = B.flatten()

    # 筛选出非零元素的索引
    non_zero_indices = np.logical_and(vector_A != 0, vector_B != 0)

    # 使用非零元素进行相关性分析
    if np.sum(non_zero_indices) == 0:
        raise ValueError("没有非零的共同数据点，无法计算相关系数。")

    correlation, _ = pearsonr(vector_A[non_zero_indices], vector_B[non_zero_indices])

    return correlation

def main():
    # 输入文件夹路径
    root_dir = input("请输入指标文件夹的路径: ")

    # 找到所有匹配的文件
    matching_files = find_matching_files(root_dir)

    # 创建一个字典，用于存储相同被试、相同条件、相同组别的文件路径
    file_dict = {}

    # 遍历匹配的文件
    for pair, group, condition, file_path in matching_files:
        # 提取被试编号
        subject_id = re.search(r'Sub\d+', os.path.basename(file_path)).group()

        # 构造字典的键
        key = (group, condition, subject_id)

        # 如果键不存在，初始化为空列表
        if key not in file_dict:
            file_dict[key] = []

        # 将文件路径添加到列表中
        file_dict[key].append((pair, file_path))

    # 创建一个空的DataFrame，用于存储结果
    results = []

    # 遍历字典，找到相同被试、相同条件、相同组别的不同pair文件
    for key, file_list in file_dict.items():
        if len(file_list) > 1:  # 确保有多个pair
            group, condition, subject_id = key
            for i in range(len(file_list)):
                for j in range(i + 1, len(file_list)):
                    pair1, file1 = file_list[i]
                    pair2, file2 = file_list[j]
                    correlation = perform_correlation_analysis(file1, file2)
                    results.append((group, condition, subject_id, pair1, pair2, correlation))

    # 将结果转换为DataFrame
    df = pd.DataFrame(results, columns=['Group', 'Condition', 'Subject', 'Pair1', 'Pair2', 'Correlation'])

    # 将结果保存到Excel文件
    output_file = os.path.join(root_dir, 'correlation_results.xlsx')
    df.to_excel(output_file, index=False)

    print(f"结果已保存到 {output_file}")

if __name__ == "__main__":
    main()