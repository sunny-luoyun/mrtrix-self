import os
import time

def fod(path, list):
    start_time = time.time()
    for i in list:
        start_timee = time.time()
        print(f"现在开始处理{i}")
        # 估计响应函数
        print('估计响应函数')
        process = os.popen(f'dwi2response dhollander {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {path}/work/{i}/wm.txt {path}/work/{i}/gm.txt {path}/work/{i}/csf.txt -voxels {path}/work/{i}/voxels.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 估计FoD
        print('估计FoD')
        process = os.popen(f'dwi2fod msmt_csd {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif -mask {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif {path}/work/{i}/wm.txt {path}/work/{i}/wmfod.mif {path}/work/{i}/gm.txt {path}/work/{i}/gmfod.mif {path}/work/{i}/csf.txt {path}/work/{i}/csffod.mif -force')
        output = process.read()
        print(output)
        process.close()

        # 强度标准化
        print('强度标准化')
        process = os.popen(f'mtnormalise {path}/work/{i}/wmfod.mif {path}/work/{i}/wmfod_norm.mif {path}/work/{i}/csffod.mif {path}/work/{i}/csffod_norm.mif -mask {path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif -force')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mkdir -p {path}/Results/TCK_and_SIFT')
        output = process.read()
        print(output)
        process.close()


        # 开始全脑纤维追踪
        print('开始全脑纤维追踪')
        process = os.popen(
            f'tckgen -act {path}/work/{i}/T1_raw_5tt_coreg.mif -backtrack -seed_gmwmi {path}/work/{i}/gmwmSeed_coreg.mif -select 10000k {path}/work/{i}/wmfod_norm.mif {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck')
        output = process.read()
        print(output)
        process.close()

        # SIFT转换
        print('SIFT转换')
        process = os.popen(
            f'tcksift –act {path}/work/{i}/T1_raw_5tt_coreg.mif -term_number 1000000 {path}/Results/TCK_and_SIFT/{i}_tracks_10m.tck {path}/work/{i}/wmfod_norm.mif {path}/Results/TCK_and_SIFT/{i}_sift_1m.tck')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(
            f'mkdir -p {path}/Results/idicator')
        output = process.read()
        print(output)
        process.close()

        # 指标统计
        print('指标统计')
        process = os.popen(
            f'tckstats {path}/Results/TCK_and_SIFT/{i}_sift_1m.tck -output mean -output median -output count -dump {path}/Results/idicator/{i}_streamline_lengths.txt')
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



