import os
import time
import scipy.io as sio
import numpy as np
from scipy.io import savemat, loadmat
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

def show_menu():
    print("请选择需要计算生成矩阵的指标（输入对应的数字，用空格分隔）：")
    print("1. length 按纤维的长度对连接体边缘的每个贡献进行缩放")
    print("2. invlength  通过纤维长度的逆向对连接体边缘的每个贡献进行缩放")
    print("3. invnodevol 通过两个节点卷的逆数来缩放对连接体边缘的每个贡献")
    print("4. FA 生成矩阵其中连接值为“平均FA”(没做好)")
    print("0. 返回上一级")

def get_user_choices():
    while True:
        try:
            choices = input("请输入你的选择（例如：1 3）：").strip().split()
            choices = [int(choice) for choice in choices]
            if any(choice < 0 or choice > 7 for choice in choices):
                print("无效的选项，请重新输入！")
            else:
                return choices
        except ValueError:
            print("输入格式错误，请输入数字！")

def roi_run_menu(path, sub):
    while True:
        show_menu()
        choices = get_user_choices()
        print(choices)
        if 0 in choices:
            print("退出程序。")
            break
        print("你选择了以下指标：")
        for choice in choices:
            if choice == 1:
                print("length 按纤维的长度对连接体边缘的每个贡献进行缩放")
            elif choice == 2:
                print("invlength  通过纤维长度的逆向对连接体边缘的每个贡献进行缩放")
            elif choice == 3:
                print("invnodevol 通过两个节点卷的逆数来缩放对连接体边缘的每个贡献")
            elif choice == 4:
                print("FA 生成矩阵其中连接值为“平均FA”")
        r = input('是否继续（y/n）')
        if r == 'n':
            continue
        elif r == 'y':
            while True:
                alert = input('请输入图谱全称：')
                brain_mask = input('请输入脑区编号(不输入默认全脑构建) (多个脑区之间用"，"隔开)')
                print(f'你选择的图谱是：{alert}')
                if brain_mask == '':
                    print('你没有选择脑区，仅进行全脑矩阵构建')
                else:
                    print(f'你选择的脑区是{brain_mask}')
                choice1 = input('是否要继续（y/n）：')
                if choice1 == 'y':
                    print('开始处理')
                    # 构建相对路径
                    template_path = os.path.join(current_dir, 'Templates', f'{alert}')
                    start_time = time.time()
                    alert_model = alert
                    while '.' in alert_model:
                        alert_model, _ = os.path.splitext(alert_model)

                    for i in sub:
                        start_timee = time.time()
                        process = os.popen(
                            f'mkdir -p {path}/work/Map/{i}/')
                        output = process.read()
                        print(output)
                        process.close()

                        print('图谱格式转换')
                        process = os.popen(
                            f'mrconvert {template_path} {path}/work/Map/{i}/{alert_model}_change.nii.gz -datatype int32 -force')
                        output = process.read()
                        print(output)
                        process.close()

                        print(f'生成{i}矩阵')
                        for choice in choices:
                            if choice == 1:
                                print(f"{i}length矩阵")
                                process = os.popen(
                                    f'tck2connectome -symmetric -zero_diagonal -scale_length {path}/work/fiber/{i}/tracks_10m.tck {path}/work/Map/{i}/{alert_model}_change.nii.gz {path}/work/Map/{i}/{alert_model}_length_MAP.csv -tck_weights_in {path}/work/fiber/{i}/sift_coeffs_10M.txt -out_assignment {path}/work/Map/{i}/{alert_model}_assign_length.csv -force')
                                output = process.read()
                                print(output)
                                process.close()
                                csv_file = f'{path}/work/Map/{i}/{alert_model}_length_MAP.csv'  # CSV文件路径
                                NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

                                process = os.popen(
                                    f'mkdir -p {path}/Results/GlobalMap/length')
                                output = process.read()
                                print(output)
                                process.close()

                                mat_file = f'{path}/Results/GlobalMap/length/{i}_{alert_model}_length_MAP.mat'  # 输出的MAT文件路径
                                savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件 此处文件为完整的全脑图谱矩阵

                                if brain_mask == '':
                                    pass
                                else:

                                    process = os.popen(
                                        f'mkdir -p {path}/Results/ROIMap/length')
                                    output = process.read()
                                    print(output)
                                    process.close()

                                    mat_file_path = f'{path}/Results/GlobalMap/length/{i}_{alert_model}_length_MAP.mat'  # 替换为你的mat文件路径
                                    mat_data = sio.loadmat(mat_file_path)
                                    matrix_125x125 = mat_data['NetworkMatrix']  # 替换为mat文件中矩阵变量的名字


                                    # 将索引调整为Python的0-based索引
                                    node_indices = [int(i.strip()) - 1 for i in brain_mask.split(',')]

                                    # 提取子矩阵
                                    matrix_32x32 = matrix_125x125[np.ix_(node_indices, node_indices)]

                                    # 输出结果
                                    print(matrix_32x32)

                                    # 保存为新的mat文件
                                    sio.savemat(f'{path}/Results/ROIMap/length/{i}_{alert_model}_length_ROIMAP.mat', {'NetworkMatrix': matrix_32x32})

# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

                            elif choice == 2:

                                print(f"{i}invlength矩阵")
                                process = os.popen(
                                    f'tck2connectome -symmetric -zero_diagonal -scale_invlength {path}/work/fiber/{i}/tracks_10m.tck {path}/work/Map/{i}/{alert_model}_change.nii.gz {path}/work/Map/{i}/{alert_model}_invlength_MAP.csv -tck_weights_in {path}/work/fiber/{i}/sift_coeffs_10M.txt -out_assignment {path}/work/Map/{i}/{alert_model}_assign_invlength.csv -force')
                                output = process.read()
                                print(output)
                                process.close()
                                csv_file = f'{path}/work/Map/{i}/{alert_model}_invlength_MAP.csv'  # CSV文件路径
                                NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

                                process = os.popen(
                                    f'mkdir -p {path}/Results/GlobalMap/invlength')
                                output = process.read()
                                print(output)
                                process.close()

                                mat_file = f'{path}/Results/GlobalMap/invlength/{i}_{alert_model}_invlength_MAP.mat'  # 输出的MAT文件路径
                                savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件 此处文件为完整的全脑图谱矩阵

                                if brain_mask == '':
                                    pass
                                else:
                                    process = os.popen(
                                        f'mkdir -p {path}/Results/ROIMap/invlength')
                                    output = process.read()
                                    print(output)
                                    process.close()

                                    mat_file_path = f'{path}/Results/GlobalMap/invlength/{i}_{alert_model}_invlength_MAP.mat'  # 替换为你的mat文件路径
                                    mat_data = sio.loadmat(mat_file_path)
                                    matrix_125x125 = mat_data['NetworkMatrix']  # 替换为mat文件中矩阵变量的名字

                                    # 将索引调整为Python的0-based索引
                                    node_indices = [int(i.strip()) - 1 for i in brain_mask.split(',')]

                                    # 提取子矩阵
                                    matrix_32x32 = matrix_125x125[np.ix_(node_indices, node_indices)]

                                    # 输出结果
                                    print(matrix_32x32)

                                    # 保存为新的mat文件
                                    sio.savemat(f'{path}/Results/ROIMap/invlength/{i}_{alert_model}_invlength_ROIMAP.mat',
                                                {'NetworkMatrix': matrix_32x32})

                            elif choice == 3:
                                print(f"{i}invnodevol矩阵")
                                process = os.popen(
                                    f'tck2connectome -symmetric -zero_diagonal -scale_invnodevol {path}/work/fiber/{i}/tracks_10m.tck {path}/work/Map/{i}/{alert_model}_change.nii.gz {path}/work/Map/{i}/{alert_model}_invnodevol_MAP.csv -tck_weights_in {path}/work/fiber/{i}/sift_coeffs_10M.txt -out_assignment {path}/work/Map/{i}/{alert_model}_assign_invnodevol.csv -force')
                                output = process.read()
                                print(output)
                                process.close()
                                csv_file = f'{path}/work/Map/{i}/{alert_model}_invnodevol_MAP.csv'  # CSV文件路径
                                NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

                                process = os.popen(
                                    f'mkdir -p {path}/Results/GlobalMap/invnodevol')
                                output = process.read()
                                print(output)
                                process.close()

                                mat_file = f'{path}/Results/GlobalMap/invnodevol/{i}_{alert_model}_invnodevol_MAP.mat'  # 输出的MAT文件路径
                                savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件 此处文件为完整的全脑图谱矩阵

                                if brain_mask == '':
                                    pass
                                else:
                                    process = os.popen(
                                        f'mkdir -p {path}/Results/ROIMap/invnodevol')
                                    output = process.read()
                                    print(output)
                                    process.close()

                                    mat_file_path = f'{path}/Results/GlobalMap/invnodevol/{i}_{alert_model}_invnodevol_MAP.mat'  # 替换为你的mat文件路径
                                    mat_data = sio.loadmat(mat_file_path)
                                    matrix_125x125 = mat_data['NetworkMatrix']  # 替换为mat文件中矩阵变量的名字

                                    # 将索引调整为Python的0-based索引
                                    node_indices = [int(i.strip()) - 1 for i in brain_mask.split(',')]

                                    # 提取子矩阵
                                    matrix_32x32 = matrix_125x125[np.ix_(node_indices, node_indices)]

                                    # 输出结果
                                    print(matrix_32x32)

                                    # 保存为新的mat文件
                                    sio.savemat(
                                        f'{path}/Results/ROIMap/invnodevol/{i}_{alert_model}_invnodevol_ROIMAP.mat',
                                        {'NetworkMatrix': matrix_32x32})

                            elif choice == 4:
                                print(f"{i}FA矩阵")
                                '''tcksample tracks.tck FA.mif mean_FA_per_streamline.csv -stat_tck mean
                                    tck2connectome tracks.tck nodes.mif mean_FA_connectome.csv -scale_file mean_FA_per_streamline.csv -stat_edge mean
                                '''
                                process = os.popen(
                                    f'tcksample {path}/work/fiber/{i}/tracks_10m.tck {path}/Results/dt/{i}_FA.mif {path}/Results/Map/{i}_mean_FA_per_streamline.csv -stat_tck mean -force')
                                output = process.read()
                                print(output)
                                process.close()
                                process = os.popen(
                                    f'tck2connectome -zero_diagonal {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/{alert_model}_change.nii.gz {path}/Results/Map/{i}_mean_FA_connectome.csv -scale_file {path}/Results/Map/{i}_mean_FA_per_streamline.csv -stat_edge mean -force')
                                output = process.read()
                                print(output)
                                process.close()
                                csv_file = f'{path}/Results/Map/{i}_mean_FA_per_streamline.csv'  # CSV文件路径
                                NetworkMatrix = np.loadtxt(csv_file, delimiter=',')  # 读取CSV文件

                                process = os.popen(
                                    f'mkdir -p {path}/Results/GlobalMap/FA')
                                output = process.read()
                                print(output)
                                process.close()

                                mat_file = f'{path}/Results/GlobalMap/FA/{i}_{alert_model}_FA_MAP.mat'  # 输出的MAT文件路径
                                savemat(mat_file, {'NetworkMatrix': NetworkMatrix})  # 将变量保存为MAT文件 此处文件为完整的全脑图谱矩阵

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

                    break
                else:
                    continue
