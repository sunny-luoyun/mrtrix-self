import json
import math
import os
import preprocess
import subprocess
import time
from datetime import datetime

from FoD import fod
from dt_r import run_menu
from fsl_cut import fsl
from roimap import roi_run_menu


def load_specific_parameters(file_path, *keys):
    try:
        with open(file_path, "r") as file:
            parameters = json.load(file)
        specific_params = {key: parameters[key] for key in keys if key in parameters}

        if len(specific_params) == 1:
            return list(specific_params.values())[0]
        else:
            return specific_params
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到！")
        return {}
    except json.JSONDecodeError:
        print(f"文件 {file_path} 格式错误！")
        return {}


def menu():
    print("\n======== 以下是dwi批量处理界面 ========")
    print("1. 选项一：预处理")
    print("2. 选项二：切割脑区（freesurfer）")
    print("3. 选项三：提取弥散指标")
    print("4. 选项四：全脑纤维重建")
    print("5. 选项五：基于种子点纤维重建（没做好）")
    print("6. 选项六：基于纤维的脑网络构建")
    print("7. 选项七：使用说明")
    print("8. 选项八：切割脑区（fsl）")
    print("0. 选项零：返回上一级")
    print("=====================================")

def option_1():
    while True:
        print("======以下是预处理界面======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            if choice2 == 'y':
                print('开始预处理')
                preprocess.prep(input_path,li)
                break
            else:
                continue


        else:
            continue

def option_2():
    while True:
        print("======以下是切割脑区（freesurfer）界面======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            a = len(li)
            b = load_specific_parameters('sys.json', 'core')
            need_time = math.ceil(a / b) * 8
            if choice2 == 'y':
                st = time.time()
                now = datetime.now()
                print(f'{now.hour}:{now.minute}',f'现在开始切割脑区，时间较长！(大约需要{need_time}小时)')

                command = f"ls {input_path} | parallel --jobs {load_specific_parameters('sys.json', 'core')} recon-all -s {input_path}/{{}}/freesurfer{{}} -i {input_path}/{{}}/{{}}T1.nii.gz -all"
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                print(result.stdout)
                for i in li:
                    process = os.popen(
                        f"mv {load_specific_parameters('sys.json', 'core')}/subjects/freesurfer{i} {input_path}/{i}/")
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
            else:
                continue

def option_3():
    while True:
        print("======以下是提取弥散指标界面======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            if choice2 == 'y':
                run_menu(input_path, li)
                continue
            else:
                continue

def option_4():
    while True:
        print("======以下是纤维重建界面======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            if choice2 == 'y':
                fod(input_path, li)
                continue
            else:
                continue

def option_6():
    while True:
        print("======以下是基于纤维的脑网络构建界面======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            if choice2 == 'y':
                roi_run_menu(input_path, li)
                continue
            else:
                continue

def option_8():
    while True:
        print("======切割脑区（fsl）======")
        input_path = input('请输入工作路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1 == 'y':
            try:
                print('工作路径中有以下被试：')
                li = []
                full = input_path + '/pre'
                for item in sorted(os.listdir(full)):  # 使用 sorted() 排序
                    li.append(item)
                    print(item)

            except FileNotFoundError:
                print('请输入正确的路径!!!!')
                continue

            choice2 = input('是否要继续（y/n）：')
            if choice2 == 'y':
                fsl(input_path, li)
                continue
            else:
                continue

def help():
    print('---------------------使用说明------------------------------')
    print('工作路径为/home/xxx/xxx/workpath')
    print('工作路径下被试文件夹要求如下：')
    tree = """
    /home/xxx/xxx/workpath/pre
    │
    ├── Sub001
    │   ├── Sub001T1.nii.gz (结构像文件)
    │   ├── Sub001dwi.json (弥散像信息文件)
    │   ├── Sub001dwi.bvec (弥散像信息文件)
    │   ├── Sub001dwi.bval (弥散像信息文件)
    │   ├── Sub001dwi.nii.gz (弥散像文件)
    │   └── freesurferSub001/(如果要使用Dpabi预处理的数据，需要将freesurfer里每个被试的文件夹移动到这里，如果不用可以不建立此文件夹)
    │
    ├── Sub002
    │   ├── Sub002T1.nii.gz
    │   ├── Sub002dwi.json
    │   ├── Sub002dwi.bvec
    │   ├── Sub002dwi.bval
    │   ├── Sub002dwi.nii.gz
    │   └── freesurferSub002/
    │
    ├── ...
    │
    └── Sub0xx
        ├── Sub0xxT1.nii.gz
        ├── Sub0xxdwi.json
        ├── Sub0xxdwi.bvec
        ├── Sub0xxdwi.bval
        ├── Sub0xxdwi.nii.gz
        └── freesurferSub0xx/
    注意每个文件及其名字的大小写！！！！！！！！！！
    """
    print(tree)
    a = input('回车返回上一级')

def main():
    while True:
        menu()
        choice = input("请输入选项（0-8）：")
        if choice == "1":
            option_1()
        elif choice == "2":
            option_2()
        elif choice == "3":
            option_3()
        elif choice == "4":
            option_4()
        elif choice == "5":
            pass
        elif choice == "6":
            option_6()
        elif choice == "7":
            help()
        elif choice == "8":
            option_8()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")

if __name__ == "__main__":
    main()