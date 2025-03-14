import os
import time

def prep(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()

        process = os.popen(
            f'mkdir -p {path}/work/{i}')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")
        # 转换mif /1s
        print('格式转换')
        process = os.popen(f'mrconvert -fslgrad {path}/pre/{i}/{i}dwi.bvec {path}/pre/{i}/{i}dwi.bval {path}/pre/{i}/{i}dwi.nii.gz {path}/work/{i}/dwi_raw.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 降噪 /19s
        print('降噪')
        process = os.popen(f'dwidenoise {path}/work/{i}/dwi_raw.mif {path}/work/{i}/dwi_raw_denoise.mif -noise {path}/work/{i}/noiselevel.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 消除Gibbs Ring /23s
        print('消除Gibbs Ring')
        process = os.popen(f'mrdegibbs {path}/work/{i}/dwi_raw_denoise.mif {path}/work/{i}/dwi_raw_denoise_degibbs.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 建立AP-PA配对 /1s
        process = os.popen(f'dwiextract {path}/work/{i}/dwi_raw.mif - -bzero | mrconvert - -coord 3 0 {path}/work/{i}/b0_PA.mif -force')
        output = process.read()
        print(output)
        process.close()
        process = os.popen(f'dwiextract {path}/work/{i}/dwi_raw.mif - -bzero | mrconvert - -coord 3 0 {path}/work/{i}/b0_AP.mif -force')
        output = process.read()
        print(output)
        process.close()
        process = os.popen(f'mrcat {path}/work/{i}/b0_PA.mif {path}/work/{i}/b0_AP.mif {path}/work/{i}/b0_pair.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 头动矫正，变形矫正 /4m5s
        print('头动矫正，变形矫正')
        process = os.popen(f'dwifslpreproc {path}/work/{i}/dwi_raw_denoise_degibbs.mif {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr.mif -pe_dir AP -rpe_pair -se_epi {path}/work/{i}/b0_pair.mif -eddy_options " --data_is_shelled --slm=linear --niter=5 "  -force')
        output = process.read()
        print(output)
        process.close()


        # bias场矫正 /12s
        print('bias场矫正')
        process = os.popen(f'dwibiascorrect ants {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr.mif {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 剥脑壳
        print('剥脑壳')
        process = os.popen(
            f'dwi2mask {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 优化mask
        print('优化mask')
        process = os.popen(
            f'maskfilter {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask.mif dilate {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -npass 6 -force')
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
