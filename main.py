import os, complex_main, single_main, json


def menu():
    print("\n======== dwi处理 ========")
    print("1. 选项一：单一被试处理")
    print("2. 选项二：批量被试处理")
    print("3. 选项三：结果查看(mrview)")
    print("0. 选项零：退出程序")
    print("===========================")

'''
def sysinfo():
    while True:
        print("=======================================================================================================")
        print('你的CPU核心为',os.cpu_count(),'当前设置的并行线程数为',load_specific_parameters('sys.json', 'core'))
        print('f当前设置的freesurfer路径为', load_specific_parameters('sys.json', 'freepath'))
        print("=======================================================================================================")
        choice1 = input("输入1.更改并行线程\n输入2.更改freesurfer路径\n输入0.返回上一级")
        if choice1 == "0":
            break
        elif choice1 == "1":
            file_path = "sys.json"
            c = input('输入并行线程数:')
            update_parameter(file_path, 'core', c)
        elif choice1 == "2":
            file_path = "sys.json"
            c = input('输入freesurfer路径:')
            update_parameter(file_path, 'freepath', c)'''

def main():
    while True:
        menu()
        choice = input("请输入选项（0-8）：")
        if choice == "1":
            single_main.main()
        elif choice == "2":
            complex_main.main()
        elif choice == "3":
            process = os.popen(
                'mrview')
            output = process.read()
            print(output)
            process.close()
        # elif choice == "4":
           # sysinfo()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")

'''
def update_parameter(file_path, key, new_value):
    try:
        # 读取现有参数
        with open(file_path, "r") as file:
            parameters = json.load(file)

        # 修改指定参数
        parameters[key] = new_value

        # 将修改后的参数保存回文件
        with open(file_path, "w") as file:
            json.dump(parameters, file, indent=4)
        print(f"参数 '{key}' 已更新为 {new_value}")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到！")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 格式错误！")
    except KeyError:
        print(f"键 '{key}' 不存在于文件中！")

def load_specific_parameters(file_path, *keys):
    try:
        with open(file_path, "r") as file:
            parameters = json.load(file)  # 从文件中加载 JSON 数据
        # 仅提取所需的参数
        specific_params = {key: parameters[key] for key in keys if key in parameters}

        # 如果只加载了一个参数，直接返回该参数的值
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
'''


if __name__ == "__main__":
    main()