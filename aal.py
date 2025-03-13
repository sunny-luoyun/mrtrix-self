import os, time
import numpy as np
from scipy.io import savemat

def aal_model(path, sub):
    start_time = time.time()
    for i in sub:
        start_timee = time.time()
        process = os.popen(
            f'mkdir -p {path}/Results/Map')
        output = process.read()
        print(output)
        process.close()

        print(f'AAL图谱配准{i}dwi')
        process = os.popen(f'flirt -in aal.nii -ref {path}/work/{i}/mean_b0_preprocessed.nii.gz -dof 6 -cost normmi -omat {path}/work/{i}/aal_to_b0.mat -out {path}/work/{i}/aal_change.nii.gz')
        output = process.read()
        print(output)
        process.close()

        print(f'BNA图谱配准{i}dwi')
        process = os.popen(
            f'flirt -in BrainnetomeAtlas_BNA_MPM_thr25_1.25mm.nii.gz -ref {path}/work/{i}/mean_b0_preprocessed.nii.gz -dof 6 -cost normmi -omat {path}/work/{i}/bna_to_b0.mat -out {path}/work/{i}/bna_change_int.nii.gz')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrconvert {path}/work/{i}/bna_change_int.nii.gz {path}/work/{i}/bna_change.nii.gz -datatype int32')
        output = process.read()
        print(output)
        process.close()

        '''mrconvert bna_change.nii.gz bna_change_int.nii.gz -datatype int32'''


        print(f'生成{i}矩阵')

        '''1-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(f'tck2connectome -symmetric -scale_invnodevol {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/aal_change.nii.gz {path}/Results/Map/{i}_AAL_invnodevol_MAP.csv -out_assignment {path}/Results/Map/{i}_AAL_assign_invnodevol_MAP.csv')
        output = process.read()
        print(output)
        process.close()


        csv_file = f'{path}/Results/Map/{i}_AAL_invnodevol_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件


        mat_file = f'{path}/Results/Map/{i}_AAL_invnodevol_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        '''2-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(
            f'tck2connectome -symmetric -scale_length {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/aal_change.nii.gz {path}/Results/Map/{i}_AAL_length_MAP.csv -out_assignment {path}/Results/Map/{i}_AAL_assign_length_MAP.csv')
        output = process.read()
        print(output)
        process.close()

        csv_file = f'{path}/Results/Map/{i}_AAL_length_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

        mat_file = f'{path}/Results/Map/{i}_AAL_length_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        '''3-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(
            f'tck2connectome -symmetric -scale_invlength {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/aal_change.nii.gz {path}/Results/Map/{i}_AAL_invlength_MAP.csv -out_assignment {path}/Results/Map/{i}_AAL_assign_invlength_MAP.csv')
        output = process.read()
        print(output)
        process.close()

        csv_file = f'{path}/Results/Map/{i}_AAL_invlength_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

        mat_file = f'{path}/Results/Map/{i}_AAL_invlength_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        '''4-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(
            f'tck2connectome -symmetric -scale_invnodevol {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/bna_change.nii.gz {path}/Results/Map/{i}_BNA_invnodevol_MAP.csv -out_assignment {path}/Results/Map/{i}_BNA_assign_invnodevol_MAP.csv')
        output = process.read()
        print(output)
        process.close()

        csv_file = f'{path}/Results/Map/{i}_BNA_invnodevol_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

        mat_file = f'{path}/Results/Map/{i}_BNA_invnodevol_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        '''5-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(
            f'tck2connectome -symmetric -scale_length {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/bna_change.nii.gz {path}/Results/Map/{i}_BNA_length_MAP.csv -out_assignment {path}/Results/Map/{i}_BNA_assign_length_MAP.csv')
        output = process.read()
        print(output)
        process.close()

        csv_file = f'{path}/Results/Map/{i}_BNA_length_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

        mat_file = f'{path}/Results/Map/{i}_BNA_length_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        '''6-----------------------------------------------------------------------------------------------------------------------------------------------------'''
        process = os.popen(
            f'tck2connectome -symmetric -scale_invlength {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/bna_change.nii.gz {path}/Results/Map/{i}_BNA_invlength_MAP.csv -out_assignment {path}/Results/Map/{i}_BNA_assign_invlength_MAP.csv')
        output = process.read()
        print(output)
        process.close()

        csv_file = f'{path}/Results/Map/{i}_BNA_invlength_MAP.csv'  # CSV文件路径
        NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

        mat_file = f'{path}/Results/Map/{i}_BNA_invlength_MAP.mat'  # 输出的MAT文件路径
        savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件

        # 记录结束时间
        end_time = time.time()
        elapsed_time = end_time - start_timee
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        print(f"处理{i}结束，共花费时间：{hours}小时{minutes}分{seconds}秒")

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    print(f"运行结束，共花费时间：{hours}小时{minutes}分{seconds}秒")
