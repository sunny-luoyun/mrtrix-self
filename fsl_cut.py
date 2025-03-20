import os
import time

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')

def fsl(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()
        process = os.popen(
            f'mkdir -p {path}/work/cutbrainarea/{i}')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")
        # 转换T1像格式
        print('转换T1像格式')
        process = os.popen(
            f'mrconvert {path}/pre/{i}/{i}T1.nii.gz {path}/work/cutbrainarea/{i}/T1_raw.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 划分5种组织
        print('划分5种组织')
        process = os.popen(f'5ttgen fsl {path}/work/cutbrainarea/{i}/T1_raw.mif {path}/work/cutbrainarea/{i}/T1_raw_5tt.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 配准
        print('提取b0')
        process = os.popen(f'dwiextract {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif - -bzero | mrmath - mean {path}/work/cutbrainarea/{i}/mean_b0_preprocessed.mif -axis 3 -force')
        output = process.read()
        print(output)
        process.close()

        print('格式转换')
        process = os.popen(
            f'mrconvert {path}/work/cutbrainarea/{i}/mean_b0_preprocessed.mif {path}/work/cutbrainarea/{i}/mean_b0_preprocessed.nii.gz -force')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mrconvert {path}/work/cutbrainarea/{i}/T1_raw.mif {path}/work/cutbrainarea/{i}/T1_raw.nii.gz -force')
        output = process.read()
        print(output)
        process.close()

        print('结构像配MNI空间')
        process = os.popen(
            f'flirt -in {path}/work/cutbrainarea/{i}/T1_raw.nii.gz -ref {template_path} -dof 12 -out {path}/work/cutbrainarea/{i}/T1_to_MNI.nii.gz -omat {path}/work/cutbrainarea/{i}/T1_to_MNI_fsl.mat')
        output = process.read()
        print(output)
        process.close()

        print('弥散像配结构像')
        process = os.popen(
            f'flirt -in {path}/work/cutbrainarea/{i}/mean_b0_preprocessed.nii.gz -ref {template_path} -dof 6 -cost normmi -out {path}/work/cutbrainarea/{i}/dwi_to_MNI.nii.gz -omat {path}/work/cutbrainarea/{i}/dwi_to_MNI_fsl.mat')
        output = process.read()
        print(output)
        process.close()
        print('格式转换')
        process = os.popen(f'transformconvert {path}/work/cutbrainarea/{i}/T1_to_MNI_fsl.mat {path}/work/cutbrainarea/{i}/T1_raw.nii.gz {template_path} flirt_import {path}/work/cutbrainarea/{i}/T1_to_MNI_mrtrix.txt -force')
        output = process.read()
        print(output)
        process.close()
        print('格式转换')
        process = os.popen(f'transformconvert {path}/work/cutbrainarea/{i}/dwi_to_MNI_fsl.mat {path}/work/cutbrainarea/{i}/mean_b0_preprocessed.nii.gz {template_path} flirt_import {path}/work/cutbrainarea/{i}/dwi_to_MNI_mrtrix.txt -force')
        output = process.read()
        print(output)
        process.close()

        print('5tt配准')
        process = os.popen(f'mrtransform {path}/work/cutbrainarea/{i}/T1_raw_5tt.mif -linear {path}/work/cutbrainarea/{i}/T1_to_MNI_mrtrix.txt -template {template_path} {path}/work/cutbrainarea/{i}/T1_5tt_MNI.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('弥散像配准')
        process = os.popen(f'mrtransform {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif -linear {path}/work/cutbrainarea/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/cutbrainarea/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_MNI.mif -reorient_fod yes -force')
        output = process.read()
        print(output)
        process.close()

        print('mask配准')
        process = os.popen(f'mrtransform {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -linear {path}/work/cutbrainarea/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/cutbrainarea/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6_MNI.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('提取灰质分界线')
        process = os.popen(f'5tt2gmwmi {path}/work/cutbrainarea/{i}/T1_5tt_MNI.mif {path}/work/cutbrainarea/{i}/gmwmSeed_coreg.mif -force')
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
