import os
import time


def fsl(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()
        print(f"现在开始处理{i}")
        # 转换T1像格式
        print('转换T1像格式')
        process = os.popen(
            f'mrconvert {path}/pre/{i}/{i}T1.nii.gz {path}/work/{i}/T1_raw.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 划分5种组织
        print('划分5种组织')
        process = os.popen(f'5ttgen fsl {path}/work/{i}/T1_raw.mif {path}/work/{i}/T1_raw_5tt.mif')
        output = process.read()
        print(output)
        process.close()

        # 配准
        print('配准')
        process = os.popen(f'dwiextract {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif - -bzero | mrmath - mean {path}/work/{i}/mean_b0_preprocessed.mif -axis 3')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrconvert {path}/work/{i}/mean_b0_preprocessed.mif {path}/work/{i}/mean_b0_preprocessed.nii.gz')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrconvert {path}/work/{i}/T1_raw.mif {path}/work/{i}/T1_raw.nii.gz')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'flirt -in {path}/work/{i}/mean_b0_preprocessed.nii.gz -ref {path}/work/{i}/T1_raw.nii.gz -dof 6 -omat {path}/work/{i}/d2s_fsl.mat')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'transformconvert {path}/work/{i}/d2s_fsl.mat {path}/work/{i}/mean_b0_preprocessed.nii.gz {path}/work/{i}/T1_raw.mif flirt_import {path}/work/{i}/d2s_mrtrix.txt')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrtransform {path}/work/{i}/T1_raw.mif -linear {path}/work/{i}/d2s_mrtrix.txt -inverse {path}/work/{i}/T1_coreg.mif')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrtransform {path}/work/{i}/T1_raw_5tt.mif -linear {path}/work/{i}/d2s_mrtrix.txt -inverse {path}/work/{i}/T1_raw_5tt_coreg.mif')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'5tt2gmwmi {path}/work/{i}/T1_raw_5tt_coreg.mif {path}/work/{i}/gmwmSeed_coreg.mif')
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
