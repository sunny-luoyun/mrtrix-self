import os
import time

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
template_path = os.path.join(current_dir, 'Templates', 'MNI152.nii.gz')

def fod(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()

        process = os.popen(
            f'mkdir -p {path}/work/FOD/{i}')
        output = process.read()
        print(output)
        process.close()

        print(f"现在开始处理{i}")

        # 估计响应函数
        print('计算响应函数')
        process = os.popen(f'dwi2response dhollander {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {path}/work/FOD/{i}/wm.txt {path}/work/FOD/{i}/gm.txt {path}/work/FOD/{i}/csf.txt -force')
        output = process.read()
        print(output)
        process.close()

        # 估计FoD
        print('估计FoD')
        process = os.popen(f'dwi2fod msmt_csd {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {path}/work/FOD/{i}/wm.txt {path}/work/FOD/{i}/wmfod.mif {path}/work/FOD/{i}/gm.txt {path}/work/FOD/{i}/gmfod.mif {path}/work/FOD/{i}/csf.txt {path}/work/FOD/{i}/csffod.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 强度标准化
        print('强度标准化')
        process = os.popen(f'mtnormalise {path}/work/FOD/{i}/wmfod.mif {path}/work/FOD/{i}/wmfod_norm.mif {path}/work/FOD/{i}/csffod.mif {path}/work/FOD/{i}/csffod_norm.mif -mask {path}/work/preprocess/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -force')
        output = process.read()
        print(output)
        process.close()

        print('fod配准')
        process = os.popen(
            f'mrtransform {path}/work/FOD/{i}/wmfod_norm.mif -linear {path}/work/preprocess/{i}/dwi_to_MNI_mrtrix.txt -template {template_path} {path}/work/FOD/{i}/wmfod_norm_MNI.mif -reorient_fod yes -force')
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



