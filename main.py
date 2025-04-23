import os
import subprocess
import complex_main
import single_main
import Correlation

def check_for_updates():
    print("正在检查更新...")
    try:
        # 获取脚本所在的目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 切换到脚本所在的目录
        os.chdir(script_dir)
        # 执行 git fetch 命令，获取远程仓库的最新状态
        subprocess.run(['git', 'fetch', '--quiet'], check=True)

        # 获取本地分支的最新提交哈希值
        local_commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            text=True
        ).strip()

        # 获取远程分支的最新提交哈希值
        remote_commit = subprocess.check_output(
            ['git', 'rev-parse', 'origin/main'],
            text=True
        ).strip()

        # 获取本地分支和远程分支的共同祖先提交哈希值
        common_ancestor = subprocess.check_output(
            ['git', 'merge-base', 'HEAD', 'origin/main'],
            text=True
        ).strip()

        # 比较本地提交和远程提交
        if local_commit == remote_commit:
            print("当前代码已是最新版本。")
        elif common_ancestor == local_commit:
            print("检测到更新！本地分支落后于远程分支。")
            choice = input("是否更新到最新版本？(y/n): ").strip().lower()
            if choice == 'y':
                print("正在更新...")
                # 执行 git pull 命令，更新代码
                subprocess.run(['git', 'pull'], check=True)
                print("更新完成！请重新运行程序。")
                exit(0)  # 更新完成后退出程序
            else:
                print("已跳过更新。")
        else:
            print("无法确定更新状态，请手动检查。")
    except subprocess.CalledProcessError as e:
        print(f"检查更新时出错：{e}")
    except Exception as e:
        print(f"发生错误：{e}")

def menu():
    print("\n======== dwi处理 ========")
    print("1. 选项一：单一被试处理")
    print("2. 选项二：批量被试处理")
    print("3. 选项三：结果查看(mrview)")
    print("4. 选项四：矩阵相关分析")
    print("5. 选项五：使用说明")
    print("0. 选项零：退出程序")
    print("===========================")

def main():
    check_for_updates()  # 在程序开始时检查更新
    while True:
        menu()
        choice = input("请输入选项（0-5）：")
        if choice == "1":
            single_main.main()
        elif choice == "2":
            complex_main.main()
        elif choice == "3":
            process = os.popen('mrview')
            output = process.read()
            print(output)
            process.close()
        elif choice == "4":
            Correlation.main()
        elif choice == "5":
            help_()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")

def help_():
    print('---------------------使用说明-----------------------------')
    print('根据处理需求选择单一/批量被试处理')
    print('矩阵相关性分析工作路径下被试文件夹要求如下：')
    tree = """
        /home/xxx/xxx/sample(指标文件夹)
        │
        ├── Sample1 (需要做相关的两个文件夹)
        │   ├── Group1 
        │   │   ├── condition1
        │   │   │   ├── **Sub001**.mat (矩阵文件,需要有Sub及编号)
        │   │   │   ├── **Sub002**.mat (矩阵文件,需要有Sub及编号)
        │   │   ├── condition2
        │   │       ├── **Sub001**.mat (矩阵文件,需要有Sub及编号)
        │   │       ├── **Sub002**.mat (矩阵文件,需要有Sub及编号)
        │   ├── Group2 
        │       ├── condition1
        │       │   ├── **Sub001**.mat (矩阵文件,需要有Sub及编号)
        │       │   ├── **Sub002**.mat (矩阵文件,需要有Sub及编号)
        │       ├── condition2
        │           ├── **Sub001**.mat (矩阵文件,需要有Sub及编号)
        │           ├── **Sub002**.mat (矩阵文件,需要有Sub及编号)
        │
        ├── Sample2 (需要做相关的两个文件夹)
        │   ├── Group1 
        │   │   ├── condition1
        │   │   ├── condition2
        │   ├── Group2
        │       ├── condition1
        │       ├── condition2
        """
    print(tree)
    input('按回车返回上一级')

if __name__ == "__main__":
    main()