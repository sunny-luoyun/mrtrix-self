import time, os
def menu_c(input_path, li):
    fn = input('选择构建的纤维数量（单位k）')
    sst = time.time()
    for i in li:
        st = time.time()
        print(f'开始{i}纤维构建')
        process = os.popen(f'dwi2response msmt_5tt {input_path}/{i}/biascorr.mif {input_path}/{i}/5ttseg.mif {input_path}/{i}/ms_5tt_wm.txt {input_path}/{i}/ms_5tt_gm.txt {input_path}/{i}/ms_5tt_csf.txt -force')
        output = process.read()
        print(output)
        process.close()

        print('Csd 生成')
        process = os.popen(f'dwi2fod msmt_csd {input_path}/{i}/biascorr.mif \
        	{input_path}/{i}/ms_5tt_wm.txt {input_path}/{i}/dwi_wmCsd.mif \
        	{input_path}/{i}/ms_5tt_gm.txt {input_path}/{i}/dwi_gmCsd.mif \
        	{input_path}/{i}/ms_5tt_csf.txt {input_path}/{i}/dwi_csfCsd.mif -force')
        output = process.read()
        print(output)
        process.close()
        print(f'开始{i}纤维构建')
        process = os.popen(
            f'mrthreshold -abs 0.2 {input_path}/{i}/dt_fa.mif - | mrcalc - {input_path}/{i}/dwi_mask.mif -mult {input_path}/{i}/dwi_wmMask.mif -force')
        output = process.read()
        print(output)
        process.close()

        process = os.popen(f'tckgen -algo iFOD2 -act {input_path}/{i}/5ttseg.mif -backtrack -crop_at_gmwmi \
        	-cutoff 0.05 -angle 45 -minlength 20 -maxlength 200 \
                -seed_image {input_path}/{i}/dwi_wmMask.mif -select {fn}k \
               {input_path}/{i}/dwi_wmCsd.mif \
               {input_path}/{i}/fibs_{fn}k_angle45_maxlen200_act.tck')
        output = process.read()
        print(output)
        process.close()

        et = time.time()
        elapsed_time = et - st
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        print(f"{i}处理结束，共花费时间：{hours}小时{minutes}分{seconds}秒")

    eet = time.time()
    elapsed_time = eet - sst
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    print(f"全部处理结束，共花费时间：{hours}小时{minutes}分{seconds}秒")
