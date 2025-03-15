import os, preprocess, json
import dt_r, FoD, roimap, fsl_cut

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
    print("2. 选项二：切割脑区（fsl）")
    print("3. 选项三：提取弥散指标")
    print("4. 选项四：全脑纤维重建")
    print("5. 选项五：基于种子点纤维重建（没做好）")
    print("6. 选项六：基于纤维的脑网络构建")
    print("7. 选项七：使用说明")
    print("0. 选项零：返回上一级")
    print("=====================================")


def option_1():
    while True:
        print("======以下是预处理界面======")
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1.lower() == 'y':  # 转换为小写，增加容错性
            try:
                # 获取被试文件夹名称
                subject_name = input('请输入要处理的被试文件夹名称：')
                full_path = os.path.join(input_path, 'pre', subject_name)  # 构造完整路径
                if os.path.isdir(full_path):  # 检查文件夹是否存在
                    print(f'找到被试文件夹：{subject_name}')
                    subject_list = [subject_name]  # 创建只包含一个被试名称的列表
                    print('开始预处理')
                    print(input_path, subject_list)
                    preprocess.prep(input_path, subject_list)  # 调用预处理函数
                    break
                else:
                    print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
                    continue
            except Exception as e:
                print(f'发生错误：{e}')
                continue
        else:
            continue

def option_3():
    while True:
        print("======以下是提取弥散指标界面======")
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1.lower() == 'y':  # 转换为小写，增加容错性
            try:
                # 获取被试文件夹名称
                subject_name = input('请输入要处理的被试文件夹名称：')
                full_path = os.path.join(input_path, 'pre', subject_name)  # 构造完整路径
                if os.path.isdir(full_path):  # 检查文件夹是否存在
                    print(f'找到被试文件夹：{subject_name}')
                    subject_list = [subject_name]  # 创建只包含一个被试名称的列表
                    print('开始预处理')
                    print(input_path, subject_list)
                    dt_r.run_menu(input_path, subject_list)  # 调用预处理函数
                    break
                else:
                    print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
                    continue
            except Exception as e:
                print(f'发生错误：{e}')
                continue
        else:
            continue


def option_4():
    while True:
        print("======以下是纤维重建界面======")
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1.lower() == 'y':  # 转换为小写，增加容错性
            try:
                # 获取被试文件夹名称
                subject_name = input('请输入要处理的被试文件夹名称：')
                full_path = os.path.join(input_path, 'pre', subject_name)  # 构造完整路径
                if os.path.isdir(full_path):  # 检查文件夹是否存在
                    print(f'找到被试文件夹：{subject_name}')
                    subject_list = [subject_name]  # 创建只包含一个被试名称的列表
                    print('开始预处理')
                    print(input_path, subject_list)
                    FoD.fod(input_path, subject_list)  # 调用预处理函数
                    break
                else:
                    print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
                    continue
            except Exception as e:
                print(f'发生错误：{e}')
                continue
        else:
            continue

def option_6():
    while True:
        print("======以下是基于纤维的脑网络构建界面======")
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1.lower() == 'y':  # 转换为小写，增加容错性
            try:
                # 获取被试文件夹名称
                subject_name = input('请输入要处理的被试文件夹名称：')
                full_path = os.path.join(input_path, 'pre', subject_name)  # 构造完整路径
                if os.path.isdir(full_path):  # 检查文件夹是否存在
                    print(f'找到被试文件夹：{subject_name}')
                    subject_list = [subject_name]  # 创建只包含一个被试名称的列表
                    print('开始预处理')
                    print(input_path, subject_list)
                    roimap.roi_run_menu(input_path, subject_list)  # 调用预处理函数
                    break
                else:
                    print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
                    continue
            except Exception as e:
                print(f'发生错误：{e}')
                continue
        else:
            continue

def option_2():
    while True:
        print("======切割脑区（fsl）======")
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice1 = input('是否要继续（y/n）：')
        if choice1.lower() == 'y':  # 转换为小写，增加容错性
            try:
                # 获取被试文件夹名称
                subject_name = input('请输入要处理的被试文件夹名称：')
                full_path = os.path.join(input_path, 'pre', subject_name)  # 构造完整路径
                if os.path.isdir(full_path):  # 检查文件夹是否存在
                    print(f'找到被试文件夹：{subject_name}')
                    subject_list = [subject_name]  # 创建只包含一个被试名称的列表
                    print('开始预处理')
                    print(input_path, subject_list)
                    fsl_cut.fsl(input_path, subject_list)  # 调用预处理函数
                    break
                else:
                    print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
                    continue
            except Exception as e:
                print(f'发生错误：{e}')
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
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")


if __name__ == "__main__":
    main()
