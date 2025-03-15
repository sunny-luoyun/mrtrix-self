import json, os
from FoD import fod
from dt_r import run_menu
from fsl_cut import fsl
from roimap import roi_run_menu
from preprocess import prep


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
    print("1. 预处理")
    print("2. 切割脑区（fsl）")
    print("3. 提取弥散指标")
    print("4. 全脑纤维重建")
    print("5. 基于种子点纤维重建（未完成）")
    print("6. 基于纤维的脑网络构建")
    print("7. 使用说明")
    print("0. 返回上一级")
    print("=====================================")


def get_input_path():
    while True:
        input_path = input('请输入工作路径(输入0返回上一级): ')
        if input_path == "0":
            return None
        try:
            full_path = os.path.join(input_path, 'pre')
            subjects = sorted(os.listdir(full_path))
            print(f'工作路径中有以下被试：')
            for subject in subjects:
                print(subject)
            return input_path, subjects
        except FileNotFoundError:
            print('请输入正确的路径!!!!')


def option_preprocess(input_path, subjects):
    print('开始预处理')
    prep(input_path, subjects)


def option_fsl(input_path, subjects):
    fsl(input_path, subjects)


def option_extract_metrics(input_path, subjects):
    run_menu(input_path, subjects)


def option_fiber_reconstruction(input_path, subjects):
    fod(input_path, subjects)


def option_brain_network(input_path, subjects):
    roi_run_menu(input_path, subjects)


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
    │   └── freesurferSub001
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
    input('按回车返回上一级')


def main():
    while True:
        menu()
        choice = input("请输入选项（0-7）：")
        if choice == "0":
            break
        elif choice in ["1", "2", "3", "4", "6"]:
            input_path, subjects = get_input_path()
            if input_path is None:
                continue
            if choice == "1":
                option_preprocess(input_path, subjects)
            elif choice == "2":
                option_fsl(input_path, subjects)
            elif choice == "3":
                option_extract_metrics(input_path, subjects)
            elif choice == "4":
                option_fiber_reconstruction(input_path, subjects)
            elif choice == "6":
                option_brain_network(input_path, subjects)
        elif choice == "5":
            print("该功能尚未完成！")
        elif choice == "7":
            help()
        else:
            print("无效的选项，请重新输入！")


if __name__ == "__main__":
    main()