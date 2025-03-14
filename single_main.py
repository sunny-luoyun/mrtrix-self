import os, preprocess, subprocess, json
from datetime import datetime
from dt_r import run_menu
from confiber import menu_c
import time
# 测试能否使用

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
    print("\n======== 以下是dwi单一处理界面 ========")
    print("1. 选项一：预处理")
    print("2. 选项二：切割脑区（freesurfer）")
    print("3. 选项三：提取弥散指标")
    print("4. 选项四：全脑纤维重建")
    print("5. 选项五：基于种子点纤维重建（没做好）")
    print("6. 选项六：基于纤维的脑网络构建（没做好）")
    print("7. 选项七：使用说明")
    print("0. 选项零：返回上一级")
    print("=====================================")


def option_1():
    while True:
        print("======以下是预处理界面======")
        input_path = input('请输入被试文件夹路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的被试文件夹是：{input_path}')
        directory, folder = os.path.split(input_path)
        li = []
        li.append(folder)
        choice2 = input('是否要继续（y/n）：')
        if choice2 == 'y':
            print('开始预处理')
            preprocess.prep(directory, li)
            break
        else:
            continue


def option_2():
    while True:
        print("======以下是切割脑区（freesurfer）界面======")
        input_path = input('请输入被试文件夹路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的被试文件夹是：{input_path}')
        directory, folder = os.path.split(input_path)

        choice2 = input('是否要继续（y/n）：')
        if choice2 == 'y':
            st = time.time()
            now = datetime.now()
            print(now.hour, now.minute, '现在开始切割脑区，时间较长！')

            command = f"recon-all -i {folder}.nii.gz -subjid {input_path}/freesurfer{folder} -sd . -all"
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)

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
        input_path = input('请输入被试文件夹路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的被试文件夹是：{input_path}')
        directory, folder = os.path.split(input_path)
        li = []
        li.append(folder)
        choice2 = input('是否要继续（y/n）：')
        if choice2 == 'y':
            run_menu(directory, li)
            continue
        else:
            continue


def option_4():
    while True:
        print("======以下是纤维重建界面======")
        input_path = input('请输入被试文件夹路径(输入0返回上一级):')
        if input_path == "0":
            break
        print(f'你的被试文件夹是：{input_path}')
        directory, folder = os.path.split(input_path)
        li = []
        li.append(folder)
        choice2 = input('是否要继续（y/n）：')
        if choice2 == 'y':
            menu_c(directory, li)
            continue
        else:
            continue


def help():
    print('---------------------使用说明------------------------------')
    print('工作路径为/home/xxx/xxx/xxx/Sub001')
    print('工作路径下被试文件夹要求如下：')
    tree = """
    /home/xxx/xxx/xxx/Sub001
        │
        ├── Sub001T1.nii.gz (结构像文件)
        ├── Sub001dwi.json (弥散像信息文件)
        ├── Sub001dwi.bvec (弥散像信息文件)
        ├── Sub001dwi.bval (弥散像信息文件)
        ├── Sub001dwi.nii.gz (弥散像文件)
        └── freesurferSub001/(如果要使用Dpabi预处理的数据，需要将freesurfer里每个被试的文件夹移动到这里，如果不用可以不建立此文件夹)
  
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
            pass
        elif choice == "7":
            help()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")


if __name__ == "__main__":
    main()
