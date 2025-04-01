import os
import time

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')

def fiber(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()

        process = os.popen(
            f'mkdir -p {path}/work/fiber/{i}')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")

        print('mask配准')
        process = os.popen(f'mrtransform {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -linear {path}/work/preprocess/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/fiber/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6_MNI.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 开始全脑纤维追踪
        print('开始全脑纤维追踪')
        process = os.popen(
            f'tckgen -act {path}/work/preprocess/{i}/T1_MNI_5tt.mif -backtrack -seed_gmwmi {path}/work/preprocess/{i}/gmwmSeed.mif -select 10000k {path}/work/FOD/{i}/wmfod_norm_MNI.mif {path}/work/fiber/{i}/tracks_10m.tck')
        output = process.read()
        print(output)
        process.close()

        print('缩减纤维数量')
        process = os.popen(
            f'tcksift –act {path}/work/preprocess/{i}/T1_MNI_5tt.mif -term_number 1000k {path}/work/fiber/{i}/tracks_10m.tck {path}/work/FOD/{i}/wmfod_norm_MNI.mif {path}/work/fiber/{i}/sift_1m.tck')
        output = process.read()
        print(output)
        process.close()

        print('计算纤维权重')
        process = os.popen(
            f'tcksift2 –act {path}/work/preprocess/{i}/T1_MNI_5tt.mif {path}/work/fiber/{i}/tracks_10m.tck {path}/work/FOD/{i}/wmfod_norm_MNI.mif {path}/work/fiber/{i}/sift_coeffs_10M.txt')
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
