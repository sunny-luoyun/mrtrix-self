import os, complex_main, single_main, Correlation


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
        elif choice == "4":
            Correlation.main()
        elif choice == "5":
            help_()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")

def help_():
    print('---------------------使用说明------------------------------')
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