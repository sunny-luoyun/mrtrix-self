import os
import time

from numpy.random import choice

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')


def FC(path, list):
    while True:
        roi_input = input('输入ROI（可以是MNI坐标 x,y,z 或 mask文件路径）：')

        # 判断输入是坐标还是文件
        if os.path.isfile(roi_input):
            # 如果是文件，直接使用-seed_image方法
            seed_method = f'-seed_image {roi_input}'
        else:
            # 如果是坐标，解析坐标
            try:
                coords = roi_input.replace(',', ' ').split()
                x, y, z = float(coords[0]), float(coords[1]), float(coords[2])

                # 输入半径
                r = input('输入半径：')
                r = float(r)

                # 使用-seed_sphere方法
                seed_method = f'-seed_sphere {x},{y},{z},{r}'
            except (ValueError, IndexError):
                print("输入格式错误，请重新输入")
                continue

        smooth = int(input('对结果进行高斯平滑（FWHM）单位mm，输入0则不进行平滑'))

        # 确认输入
        cho = input(f'输入的种子点方法为: {seed_method}回车继续，输入0返回上一级')
        if cho == "0":
            continue
        else:
            break

    start_time = time.time()

    for i in list:
        start_timee = time.time()
        print(f"现在开始处理{i}")

        # 创建必要的目录
        os.makedirs(f'{path}/work/ROI_fiber/{i}', exist_ok=True)
        os.makedirs(f'{path}/Results/ROI_track_map', exist_ok=True)

        print('mask配准')
        os.system(
            f'mrtransform {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -linear {path}/work/preprocess/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/fiber/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6_MNI.mif -force')

        # 开始纤维追踪
        print('开始纤维追踪')
        os.system(
            f'tckgen -act {path}/work/preprocess/{i}/T1_MNI_5tt.mif -backtrack {seed_method} -select 200k {path}/work/FOD/{i}/wmfod_norm_MNI.mif {path}/work/ROI_fiber/{i}/ROI_tracks.tck')

        print('转化为MAP图')
        os.system(
            f'tckmap -contrast tdi -vox 1.0 -template {template_path} {path}/work/ROI_fiber/{i}/ROI_tracks.tck {path}/work/ROI_fiber/{i}/ROI_tracks.mif')

        if smooth == 0:
            break
        else:
            os.system(
                f'tckmap -contrast tdi -vox 1.0 -template {template_path} -fwhm_tck {smooth} {path}/work/ROI_fiber/{i}/ROI_tracks.tck {path}/work/ROI_fiber/{i}/ROI_tracks_S{smooth}.mif')

            os.makedirs(f'{path}/Results/ROI_track_S{smooth}_map', exist_ok=True)

            os.system(
                f'mrconvert {path}/work/ROI_fiber/{i}/ROI_tracks.mif {path}/Results/ROI_track_S{smooth}_map/{i}_ROI_TDI_MAP.nii')

        os.system(
            f'mrconvert {path}/work/ROI_fiber/{i}/ROI_tracks.mif {path}/Results/ROI_track_map/{i}_ROI_TDI_MAP.nii')

        # 记录处理时间
        end_time = time.time()
        elapsed_time = end_time - start_timee
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"处理{i}结束，共花费时间：{hours}小时{minutes}分{seconds}秒")

    # 总处理时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"运行结束，共花费时间：{hours}小时{minutes}分{seconds}秒")
