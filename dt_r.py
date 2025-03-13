import os, time

def show_menu():
    print("请选择需要计算的弥散像指标（输入对应的数字，用空格分隔）：")
    print("1. FA 计算扩散张量的分数各向异性（纤维构建必选*）")
    print("2. AD 计算扩散张量的轴向扩散率")
    print("3. RD 计算扩散张量的径向扩散率")
    print("4. ADC 计算扩散张量的平均表观扩散系数")
    print("5. cl 计算扩散张量的线性度量")
    print("6. cp 计算扩散张量的平面度度量")
    print("7. cs 计算扩散张量的球形度量")
    print("0. 返回上一级")


def get_user_choices():
    while True:
        try:
            choices = input("请输入你的选择（例如：1 3）：").strip().split()
            choices = [int(choice) for choice in choices]
            if any(choice < 0 or choice > 7 for choice in choices):
                print("无效的选项，请重新输入！")
            else:
                return choices
        except ValueError:
            print("输入格式错误，请输入数字！")



def run_menu(input_path, li):
    while True:
        show_menu()
        choices = get_user_choices()
        print(choices)
        if 0 in choices:
            print("退出程序。")
            break
        print("你选择了以下指标：")
        for choice in choices:
            if choice == 1:
                print("FA 计算扩散张量的分数各向异性")
            elif choice == 2:
                print("AD 计算扩散张量的轴向扩散率")
            elif choice == 3:
                print("RD 计算扩散张量的径向扩散率")
            elif choice == 4:
                print("ADC 计算扩散张量的平均表观扩散系数")
            elif choice == 5:
                print("cl 计算扩散张量的线性度量")
            elif choice == 6:
                print("cp 计算扩散张量的平面度度量")
            elif choice == 7:
                print("cs 计算扩散张量的球形度量")
        r = input('是否继续（y/n）')
        if r == 'n':
            continue
        elif r == 'y':
            st = time.time()
            '''g55t(input_path, li)'''
            process = os.popen(
                f'mkdir -p {input_path}/Results/dt')
            output = process.read()
            print(output)
            process.close()

            for i in li:
                process = os.popen(
                    f'dwi2tensor -mask {input_path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr_mask_dilate6.mif {input_path}/work/{i}/dwi_raw_denoise_degibbs_geomcorr_biascorr.mif {input_path}/work/{i}/dt.mif -force')
                output = process.read()
                print(output)
                process.close()

                for choice in choices:
                    if choice == 1:
                        print(f"FA 计算{i}扩散张量的分数各向异性")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -fa {input_path}/Results/dt/{i}_dt_fa.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 2:
                        print(f"AD 计算{i}扩散张量的轴向扩散率")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -ad {input_path}/Results/dt/{i}_dt_ad.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 3:
                        print(f"RD 计算{i}扩散张量的径向扩散率")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -rd {input_path}/Results/dt/{i}_dt_rd.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 4:
                        print(f"ADC 计算{i}扩散张量的平均表观扩散系数")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -adc {input_path}/Results/dt/{i}_dt_adc.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 5:
                        print(f"cl 计算{i}扩散张量的线性度量")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -cl {input_path}/Results/dt/{i}_dt_cl.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 6:
                        print(f"cp 计算{i}扩散张量的平面度度量")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -cp {input_path}/Results/dt/{i}_dt_cp.mif -force')
                        output = process.read()
                        print(output)
                        process.close()
                    elif choice == 7:
                        print(f"cs 计算{i}扩散张量的球形度量")
                        process = os.popen(
                            f'tensor2metric {input_path}/work/{i}/dt.mif -cs {input_path}/Results/dt/{i}_dt_cs.mif -force')
                        output = process.read()
                        print(output)
                        process.close()

            et = time.time()
            elapsed_time = et - st
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            print(f"处理结束，共花费时间：{hours}小时{minutes}分{seconds}秒")
            break
