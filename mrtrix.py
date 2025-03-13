import os
import time


start_time = time.time()
path = '/home/luo/exam'
sub = '001'

# 建立工作文件夹

process = os.popen(f'mkdir -p {path}/work/sub-Sub{sub}')
output = process.read()
print(output)
process.close()

# 55t 模板分割
process = os.popen(f'mrconvert {path}/freesurfer/sub-Sub{sub}/mri/aparc.a2009s+aseg.mgz {path}/work/sub-Sub{sub}/aparc.a2009s+aseg.nii.gz -force')
output = process.read()
print(output)
process.close()
process = os.popen(f'5ttgen freesurfer {path}/work/sub-Sub{sub}/aparc.a2009s+aseg.nii.gz {path}/work/sub-Sub{sub}/5ttseg.mif')
output = process.read()
print(output)
process.close()
process = os.popen(f'5tt2gmwmi {path}/work/sub-Sub{sub}/5ttseg.mif {path}/work/sub-Sub{sub}/5tt_gmwmi.mif')
output = process.read()
print(output)
process.close()

# 转换成mif

process = os.popen(f'mrconvert -fslgrad {path}/qsiprep/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_dwi.bvec {path}/qsiprep/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_dwi.bval {path}/qsiprep/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_dwi.nii.gz {path}/work/sub-Sub{sub}/align.mif -force')
output = process.read()
print(output)
process.close()

# 建立mask

process = os.popen(f'dwi2mask {path}/work/sub-Sub{sub}/align.mif - | maskfilter - dilate {path}/work/sub-Sub{sub}/dwi_mask.mif  -force')
output = process.read()
print(output)
process.close()

# 建立弥散张量

process = os.popen(f'dwi2tensor -mask {path}/work/sub-Sub{sub}/dwi_mask.mif {path}/work/sub-Sub{sub}/align.mif {path}/work/sub-Sub{sub}/dt.mif -force')
output = process.read()
print(output)
process.close()

# 计算弥散张量数据（FA，AD）

process = os.popen(f'tensor2metric {path}/work/sub-Sub{sub}/dt.mif -fa {path}/work/sub-Sub{sub}/dt_fa.mif -ad {path}/work/sub-Sub{sub}/dt_ad.mif -force')
output = process.read()
print(output)
process.close()

# 反卷积计算弥散张量数据（CSD）

process = os.popen(f'dwi2response msmt_5tt {path}/work/sub-Sub{sub}/align.mif {path}/work/sub-Sub{sub}/5ttseg.mif {path}/work/sub-Sub{sub}/ms_5tt_wm.txt {path}/work/sub-Sub{sub}/ms_5tt_gm.txt {path}/work/sub-Sub{sub}/ms_5tt_csf.txt -force')
output = process.read()
print(output)
process.close()

# 输出纤维构建文件FoD
process = os.popen(f'dwi2fod msmt_csd {path}/work/sub-Sub{sub}//align.mif \
	{path}/work/sub-Sub{sub}/ms_5tt_wm.txt {path}/work/sub-Sub{sub}/dwi_wmCsd.mif \
	{path}/work/sub-Sub{sub}/ms_5tt_gm.txt {path}/work/sub-Sub{sub}/dwi_gmCsd.mif \
	{path}/work/sub-Sub{sub}/ms_5tt_csf.txt {path}/work/sub-Sub{sub}/dwi_csfCsd.mif ')
output = process.read()
print(output)
process.close()

# 构建全脑ROI

process = os.popen(f'mrthreshold -abs 0.2 {path}/work/sub-Sub{sub}/dt_fa.mif - | mrcalc - {path}/work/sub-Sub{sub}/dwi_mask.mif -mult {path}/work/sub-Sub{sub}/dwi_wmMask.mif')
output = process.read()
print(output)
process.close()

# 全脑纤维重建
process = os.popen(f'tckgen -algo iFOD2 -act {path}/work/sub-Sub{sub}/5ttseg.mif -backtrack -crop_at_gmwmi \
	-cutoff 0.05 -angle 45 -minlength 20 -maxlength 200 \
        -seed_image {path}/work/sub-Sub{sub}/dwi_wmMask.mif -select 200k \
       {path}/work/sub-Sub{sub}/dwi_wmCsd.mif \
       {path}/work/sub-Sub{sub}/fibs_200k_angle45_maxlen200_act.tck')
output = process.read()
print(output)
process.close()

# 建立输出文件夹

process = os.popen(f'mkdir -p {path}/qsirecon/sub-Sub{sub}/dwi')
output = process.read()
print(output)
process.close()
process = os.popen(f'mkdir -p {path}/qsirecon/sub-Sub{sub}/anat')
output = process.read()
print(output)
process.close()

# 输出结果
process = os.popen(f'mrconvert {path}/work/sub-Sub{sub}/dwi_wmCsd.mif {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-wmFODmtnormed_ss3tcsd.mif.gz')
output = process.read()
print(output)
process.close()
process = os.popen(f'mrconvert {path}/work/sub-Sub{sub}/dwi_gmCsd.mif {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-gmFODmtnormed_ss3tcsd.mif.gz')
output = process.read()
print(output)
process.close()
process = os.popen(f'mrconvert {path}/work/sub-Sub{sub}/dwi_csfCsd.mif {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-csfFODmtnormed_ss3tcsd.mif.gz')
output = process.read()
print(output)
process.close()

process = os.popen(f'cp {path}/work/sub-Sub{sub}/ms_5tt_csf.txt {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-csfFOD_ss3tcsd.txt')
output = process.read()
print(output)
process.close()
process = os.popen(f'cp {path}/work/sub-Sub{sub}/ms_5tt_gm.txt {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-gmFOD_ss3tcsd.txt')
output = process.read()
print(output)
process.close()
process = os.popen(f'cp {path}/work/sub-Sub{sub}/ms_5tt_wm.txt {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-wmFOD_ss3tcsd.txt')
output = process.read()
print(output)
process.close()

process = os.popen(f'cp {path}/work/sub-Sub{sub}/fibs_200k_angle45_maxlen200_act.tck {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-tracks_ifod2.tck')
output = process.read()
print(output)
process.close()
process = os.popen(f'mrconvert {path}/work/sub-Sub{sub}/dwi_mask.mif {path}/qsirecon/sub-Sub{sub}/dwi/sub-Sub{sub}_space-T1w_desc-preproc_desc-mtinliermask_ss3tcsd.nii.gz')
output = process.read()
print(output)
process.close()

process = os.popen(f'cp {path}/work/sub-Sub{sub}/5ttseg.mif {path}/qsirecon/sub-Sub{sub}/anat/sub-Sub{sub}_desc-preproc_space-fsnative_desc-hsvs_5tt.mif')
output = process.read()
print(output)

# 记录结束时间
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"运行结束，共花费时间：{minutes}分{seconds}秒")
