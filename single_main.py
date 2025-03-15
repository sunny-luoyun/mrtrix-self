import os
import json
import preprocess
import dt_r
import FoD
import roimap
import fsl_cut


def load_specific_parameters(file_path, *keys):
    try:
        with open(file_path, "r") as file:
            parameters = json.load(file)
        return {key: parameters[key] for key in keys if key in parameters}
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到！")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 格式错误！")
    return {}


def get_input(prompt):
    """安全地获取用户输入"""
    try:
        return input(prompt)
    except Exception as e:
        print(f"输入错误：{e}")
        return None


def get_subject_path(input_path):
    """获取被试文件夹路径"""
    subject_name = get_input('请输入要处理的被试文件夹名称：')
    if not subject_name:
        return None, None
    full_path = os.path.join(input_path, 'pre', subject_name)
    if os.path.isdir(full_path):
        print(f'找到被试文件夹：{subject_name}')
        return full_path, [subject_name]
    else:
        print(f'未找到被试文件夹：{subject_name}，请检查路径是否正确！')
        return None, None


def generic_option(input_path, func):
    """通用处理选项逻辑"""
    while True:
        print(f"======请输入工作路径或0返回上一级======")
        input_path = get_input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            break
        print(f'你的工作路径是：{input_path}')
        choice = get_input('是否要继续（y/n）：').lower()
        if choice == 'y':
            full_path, subject_list = get_subject_path(input_path)
            if full_path:
                print('开始处理')
                func(input_path, subject_list)
                break
        else:
            continue


def menu():
    """显示菜单"""
    print("\n======== 以下是dwi单一处理界面 ========")
    print("1. 选项一：预处理")
    print("2. 选项二：切割脑区（fsl）")
    print("3. 选项三：提取弥散指标")
    print("4. 选项四：全脑纤维重建")
    print("5. 选项五：基于种子点纤维重建（未实现）")
    print("6. 选项六：基于纤维的脑网络构建")
    print("7. 选项七：使用说明")
    print("0. 选项零：返回上一级")
    print("=====================================")


def help():
    """显示帮助信息"""
    print('---------------------使用说明------------------------------')
    print('工作路径为/home/xxx/xxx/workpath')
    print('工作路径下被试文件夹要求如下：')
    print("""
    /home/xxx/xxx/workpath/pre
    │
    ├── Sub001
    │   ├── Sub001T1.nii.gz (结构像文件)
    │   ├── Sub001dwi.json (弥散像信息文件)
    │   ├── Sub001dwi.bvec (弥散像信息文件)
    │   ├── Sub001dwi.bval (弥散像信息文件)
    │   ├── Sub001dwi.nii.gz (弥散像文件)
    注意每个文件及其名字的大小写！！！！！！！！！！
    """)
    input('回车返回上一级')


def main():
    """主程序入口"""
    options = {
        "1": lambda: generic_option(None, preprocess.prep),
        "2": lambda: generic_option(None, fsl_cut.fsl),
        "3": lambda: generic_option(None, dt_r.run_menu),
        "4": lambda: generic_option(None, FoD.fod),
        "5": lambda: print("该功能尚未实现！"),
        "6": lambda: generic_option(None, roimap.roi_run_menu),
        "7": help
    }

    while True:
        menu()
        choice = get_input("请输入选项（0-7）：")
        if choice == "0":
            print("退出程序。")
            break
        elif choice in options:
            options[choice]()
        else:
            print("无效的选项，请重新输入！")


if __name__ == "__main__":
    main()