import os
import time

from numpy.random import choice

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')

def FC(path, list):

    while True:
        roi = input('输入ROI的MNI坐标（格式为 x,y,z 或 x y z）：')
        coords = roi.replace(',', ' ').split()
        x, y, z = float(coords[0]), float(coords[1]), float(coords[2])
        r = input('输入半径')
        r = float(r)
        cho = input(f'输入ROI为:{x, y, z} 半径为:{r} \n回车继续，输入0返回上一级')
        if cho == "0":
            continue
        else:
            break

    start_time = time.time()

    for i in list:
        start_timee = time.time()
        print(f"现在开始处理{i}")

        process = os.popen(
            f'mkdir -p {path}/work/ROI_fiber/{i}')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mkdir -p {path}/Results/ROI_track_map')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")

        print('mask配准')
        process = os.popen(
            f'mrtransform {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -linear {path}/work/preprocess/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/fiber/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6_MNI.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 开始纤维追踪
        print('开始纤维追踪')
        process = os.popen(
            f'tckgen -act {path}/work/preprocess/{i}/T1_MNI_5tt.mif -backtrack -seed_sphere {x,y,z,r} -select 200k {path}/work/FOD/{i}/wmfod_norm_MNI.mif {path}/work/ROI_fiber/{i}/ROI_tracks.tck')
        output = process.read()
        print(output)
        process.close()

        print('转化为MAP图')
        process = os.popen(
            f'tckmap -contrast tdi -vox 1.0 {path}/work/ROI_fiber/{i}/ROI_tracks.tck {path}/work/ROI_fiber/{i}/ROI_tracks.mif')
        output = process.read()
        print(output)
        process.close()

        print('格式转换')
        process = os.popen(
            f'mrconvert {path}/work/ROI_fiber/{i}/ROI_tracks.mif {path}/Results/ROI_track_map/{i}_ROI_TDI_MAP.nii')
        output = process.read()
        print(output)
        process.close()

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
