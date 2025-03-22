import os
import time

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')

def prep(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()

        process = os.popen(
            f'mkdir -p {path}/work/preprocess/{i}')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")
        # 转换mif /1s
        print('格式转换')
        process = os.popen(f'mrconvert -fslgrad {path}/pre/{i}/{i}dwi.bvec {path}/pre/{i}/{i}dwi.bval {path}/pre/{i}/{i}dwi.nii.gz {path}/work/preprocess/{i}/dwi_raw.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 降噪 /19s
        print('降噪')
        process = os.popen(f'dwidenoise {path}/work/preprocess/{i}/dwi_raw.mif {path}/work/preprocess/{i}/dwi_raw_denoise.mif -noise {path}/work/preprocess/{i}/noiselevel.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 消除Gibbs Ring /23s
        print('消除Gibbs Ring')
        process = os.popen(f'mrdegibbs {path}/work/preprocess/{i}/dwi_raw_denoise.mif {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 建立AP-PA配对 /1s
        process = os.popen(f'dwiextract {path}/work/preprocess/{i}/dwi_raw.mif - -bzero | mrconvert - -coord 3 0 {path}/work/preprocess/{i}/b0_PA.mif -force')
        output = process.read()
        print(output)
        process.close()
        process = os.popen(f'dwiextract {path}/work/preprocess/{i}/dwi_raw.mif - -bzero | mrconvert - -coord 3 0 {path}/work/preprocess/{i}/b0_AP.mif -force')
        output = process.read()
        print(output)
        process.close()
        process = os.popen(f'mrcat {path}/work/preprocess/{i}/b0_PA.mif {path}/work/preprocess/{i}/b0_AP.mif {path}/work/preprocess/{i}/b0_pair.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 头动矫正，变形矫正 /4m5s
        print('头动矫正，变形矫正')
        process = os.popen(f'dwifslpreproc {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs.mif {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr.mif -pe_dir AP -rpe_pair -se_epi {path}/work/preprocess/{i}/b0_pair.mif -eddy_options " --data_is_shelled --slm=linear --niter=5 "  -force')
        output = process.read()
        print(output)
        process.close()


        # bias场矫正 /12s
        print('bias场矫正')
        process = os.popen(f'dwibiascorrect ants {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr.mif {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('T1格式转换')
        process = os.popen(
            f'mrconvert {path}/pre/{i}/{i}T1.nii.gz {path}/work/preprocess/{i}/T1_raw.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('提取b0')
        process = os.popen(
            f'dwiextract {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif - -bzero | mrmath - mean {path}/work/preprocess/{i}/mean_b0_preprocessed.mif -axis 3 -force')
        output = process.read()
        print(output)
        process.close()

        print('b0格式转换')
        process = os.popen(
            f'mrconvert {path}/work/preprocess/{i}/mean_b0_preprocessed.mif {path}/work/preprocess/{i}/mean_b0_preprocessed.nii.gz -force')
        output = process.read()
        print(output)
        process.close()

        print('T1格式转换')
        process = os.popen(
            f'mrconvert {path}/work/preprocess/{i}/T1_raw.mif {path}/work/preprocess/{i}/T1_raw.nii.gz -force')
        output = process.read()
        print(output)
        process.close()

        print('T1配MNI空间')
        process = os.popen(
            f'flirt -in {path}/work/preprocess/{i}/T1_raw.nii.gz -ref {template_path} -dof 12 -out {path}/work/preprocess/{i}/T1_to_MNI.nii.gz -omat {path}/work/preprocess/{i}/T1_to_MNI_fsl.mat')
        output = process.read()
        print(output)
        process.close()

        print('dwi配MNI空间')
        process = os.popen(
            f'flirt -in {path}/work/preprocess/{i}/mean_b0_preprocessed.nii.gz -ref {template_path} -dof 6 -out {path}/work/preprocess/{i}/dwi_to_MNI.nii.gz -omat {path}/work/preprocess/{i}/dwi_to_MNI_fsl.mat')
        output = process.read()
        print(output)
        process.close()

        print('矩阵格式转换')
        process = os.popen(
            f'transformconvert {path}/work/preprocess/{i}/T1_to_MNI_fsl.mat {path}/work/preprocess/{i}/T1_raw.nii.gz {template_path} flirt_import {path}/work/preprocess/{i}/T1_to_MNI_mrtrix.txt -force')
        output = process.read()
        print(output)
        process.close()

        print('矩阵格式转换')
        process = os.popen(
            f'transformconvert {path}/work/preprocess/{i}/dwi_to_MNI_fsl.mat {path}/work/preprocess/{i}/mean_b0_preprocessed.nii.gz {template_path} flirt_import {path}/work/preprocess/{i}/dwi_to_MNI_mrtrix.txt -force')
        output = process.read()
        print(output)
        process.close()

        print('提取mask')
        process = os.popen(
            f'dwi2mask {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('优化mask')
        process = os.popen(
            f'maskfilter {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask.mif dilate {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -npass 6 -force')
        output = process.read()
        print(output)
        process.close()

        print('划分5种组织')
        process = os.popen(
            f'5ttgen fsl {path}/work/preprocess/{i}/T1_to_MNI.nii.gz {path}/work/preprocess/{i}/T1_MNI_5tt.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('提取灰白质分界线')
        process = os.popen(
            f'5tt2gmwmi {path}/work/preprocess/{i}/T1_MNI_5tt.mif {path}/work/preprocess/{i}/gmwmSeed.mif -force')
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
